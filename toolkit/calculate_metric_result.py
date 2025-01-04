
import os
import cv2
import numpy as np
from medpy.metric import binary


# prediction result path
project_root_path = '.../U-Net/'

# ground truth result path
gt_root_path = '.../FOCUS/testing/'

# the results of multiple experiments
n_cardiac_dsc_list = []
n_thoracic_dsc_list = []
n_cardiac_hd95_list = []
n_thoracic_hd95_list = []
n_ctr_list = []


for n_times in range(0, 10):
    result_folder_path = os.path.join(project_root_path, 'Times=%02d' % n_times)

    cardiac_dice_list, cardiac_hd95_list, thoracic_dice_list, thoracic_hd95_list, ctr_list = [], [], [], [], []
    for case_i in range(1, 51):

        # load image
        cv_image = cv2.imread(os.path.join(gt_root_path, 'images', '%03d.png' % case_i))

        # load prediction result
        prediction_txt_file = os.path.join(project_root_path, 'Times=%02d' % n_times, '%03d.txt' % case_i)
        prediction_param_dict = {}
        with open(prediction_txt_file, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                items = line.strip().split(' ')
                x, y, a, b, theta, class_name = float(items[0]), float(items[1]), float(items[2]), float(items[3]), float(items[4]), items[5]
                prediction_param_dict[class_name] = (x, y, a, b, theta)

        # get prediction mask
        prediction_mask_dict = {}
        for k, v in prediction_param_dict.items():
            c_x, c_y, a, b, theta = v
            mask = np.zeros((cv_image.shape[0], cv_image.shape[1], 3), dtype=np.uint8)
            items = line.strip().split(' ')
            obj_class = items[-1].strip()
            color = (255, 255, 255)
            mask = cv2.ellipse(mask, (int(c_x+0.5), int(c_y+0.5)), (int(a+0.5), int(b+0.5)), int(theta+0.5), 0, 360, color, -1)
            mask = mask[..., 0]
            mask[mask != 0] = 1
            prediction_mask_dict[k] = mask

        # load ground truth
        gt_param_dict = {}
        gt_txt_file = os.path.join(gt_root_path, 'annfiles_ellipse', '%03d.txt' % case_i)
        with open(gt_txt_file, mode='r', encoding='utf-8') as f:
            for line in f.readlines():
                items = line.strip().split(' ')
                x, y, a, b, theta, class_name = float(items[0]), float(items[1]), float(items[2]), float(items[3]), float(items[4]), items[5]
                gt_param_dict[class_name] = (x, y, a, b, theta)

        # get ground truth mask
        gt_mask_dict = {}
        for k, v in gt_param_dict.items():
            c_x, c_y, a, b, theta = v
            mask = np.zeros((cv_image.shape[0], cv_image.shape[1], 3), dtype=np.uint8)
            items = line.strip().split(' ')
            obj_class = items[-1].strip()
            color = (255, 255, 255)
            mask = cv2.ellipse(mask, (int(c_x+0.5), int(c_y+0.5)), (int(a+0.5), int(b+0.5)), int(theta+0.5), 0, 360, color, -1)
            mask = mask[..., 0]
            mask[mask != 0] = 1
            gt_mask_dict[k] = mask

        # metric calculation: Dice and HD95
        cardiac_dice = binary.dc(prediction_mask_dict['cardiac'], gt_mask_dict['cardiac'])
        thoracic_dice = binary.dc(prediction_mask_dict['thoracic'], gt_mask_dict['thoracic'])
        cardiac_hd95 = binary.hd95(prediction_mask_dict['cardiac'], gt_mask_dict['cardiac'])
        thoracic_hd95 = binary.hd95(prediction_mask_dict['thoracic'], gt_mask_dict['thoracic'])
        # biometric metric：CTR
        _, _, gt_cardiac_a, gt_cardiac_b, gt_cardiac_angle = gt_param_dict['cardiac']
        _, _, gt_thoracic_a, gt_thoracic_b, gt_thoracic_angle = gt_param_dict['thoracic']
        gt_ctr = gt_cardiac_b / gt_thoracic_b
        _, _, prediction_cardiac_a, prediction_cardiac_b, prediction_cardiac_angle = prediction_param_dict['cardiac']
        _, _, prediction_thoracic_a, prediction_thoracic_b, prediction_thoracic_angle = prediction_param_dict['thoracic']
        prediction_ctr = prediction_cardiac_b / prediction_thoracic_b
        ctr_mse = 1 - np.abs(gt_ctr - prediction_ctr) / gt_ctr

        cardiac_dice_list.append(cardiac_dice)
        cardiac_hd95_list.append(cardiac_hd95)
        thoracic_dice_list.append(thoracic_dice)
        thoracic_hd95_list.append(thoracic_hd95)
        ctr_list.append(ctr_mse)

    n_cardiac_dsc_list.append(np.mean(cardiac_dice_list))
    n_cardiac_hd95_list.append(np.mean(cardiac_hd95_list))
    n_thoracic_dsc_list.append(np.mean(thoracic_dice_list))
    n_thoracic_hd95_list.append(np.mean(thoracic_hd95_list))
    n_ctr_list.append(np.mean(ctr_list))

print('Thoracic DSC:')
print(np.mean(n_thoracic_dsc_list), np.std(n_thoracic_dsc_list))
print('Thoracic HD95:')
print(np.mean(n_thoracic_hd95_list), np.std(n_thoracic_hd95_list))
print('Cardiac DSC:')
print(np.mean(n_cardiac_dsc_list), np.std(n_cardiac_dsc_list))
print('Cardiac HD95:')
print(np.mean(n_cardiac_hd95_list), np.std(n_cardiac_hd95_list))
print('CTR:')
print(np.mean(n_ctr_list), np.std(n_ctr_list))

