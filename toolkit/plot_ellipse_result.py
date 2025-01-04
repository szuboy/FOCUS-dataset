
import os
import cv2
import tqdm

# prediction result path
project_root_path = '.../U-Net/Times=1'

# ground truth result path
gt_root_path = '.../FOCUS/testing/'

# visualization result save path
visualization_save_path = os.path.join(project_root_path, 'visualization_ellipse')
if not os.path.exists(visualization_save_path):
    os.makedirs(visualization_save_path)

# visualize each case
for case_i in tqdm.tqdm(range(1, 51)):

    # read image
    cv_image = cv2.imread(os.path.join(gt_root_path, 'images', '%03d.png' % case_i))

    # load ground truth
    gt_param_dict = {}
    gt_txt_file = os.path.join(gt_root_path, 'annfiles_ellipse', '%03d.txt' % case_i)
    with open(gt_txt_file, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split(' ')
            x, y, a, b, theta, class_name = float(items[0]), float(items[1]), float(items[2]), float(items[3]), float(items[4]), items[5]
            gt_param_dict[class_name] = (x, y, a, b, theta)

    # plot ground truth
    for k, v in gt_param_dict.items():
        c_x, c_y, a, b, theta = v
        items = line.strip().split(' ')
        obj_class = items[-1].strip()
        color = (255, 0, 0)
        cv_image = cv2.ellipse(cv_image, (int(c_x+0.5), int(c_y+0.5)), (int(a+0.5), int(b+0.5)), int(theta+0.5), 0, 360, color, 2)

    # load prediction result
    prediction_txt_file = os.path.join(project_root_path, '%03d.txt' % case_i)
    prediction_param_dict = {}
    with open(prediction_txt_file, mode='r', encoding='utf-8') as f:
        for line in f.readlines():
            items = line.strip().split(' ')
            x, y, a, b, theta, class_name = float(items[0]), float(items[1]), float(items[2]), float(items[3]), float(items[4]), items[5]
            prediction_param_dict[class_name] = (x, y, a, b, theta)

    # plot prediction result
    color_list = [(0, 255, 0), (0, 255, 255)]
    for k, v in prediction_param_dict.items():
        c_x, c_y, a, b, theta = v
        items = line.strip().split(' ')
        obj_class = items[-1].strip()
        color = color_list[0 if k == 'cardiac' else 1]
        cv_image = cv2.ellipse(cv_image, (int(c_x+0.5), int(c_y+0.5)), (int(a+0.5), int(b+0.5)), int(theta+0.5), 0, 360, color, 2)

    # save visualization result
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    cv2.imwrite(os.path.join(visualization_save_path, '%03d.png' % case_i), cv_image)

