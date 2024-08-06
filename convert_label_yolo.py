import os
import glob

def convert_bbox_to_yolo(x_min, y_min, x_max, y_max, img_width, img_height):
    x_center = (x_min + x_max) / 2.0 / img_width
    y_center = (y_min + y_max) / 2.0 / img_height
    width = (x_max - x_min) / img_width
    height = (y_max - y_min) / img_height
    return x_center, y_center, width, height

def convert_annotations(input_folder, output_folder, img_width, img_height):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for txt_file in glob.glob(os.path.join(input_folder, '*.txt')):
        with open(txt_file, 'r') as f:
            lines = f.readlines()

        output_lines = []
        for line in lines:
            parts = line.strip().split()
            x_min, y_min, x_max, y_max, class_id = map(int, parts)
            # 将类标签从1-6改为0-5
            class_id -= 1
            x_center, y_center, width, height = convert_bbox_to_yolo(
                x_min, y_min, x_max, y_max, img_width, img_height)
            output_lines.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")

        output_file = os.path.join(output_folder, os.path.basename(txt_file))
        with open(output_file, 'w') as f:
            f.writelines(output_lines)

# 假设图像宽度和高度
img_width = 640
img_height = 640

# 转换标注
input_folder = 'dataset/PCB/labels'
output_folder = 'dataset/PCB/labels'
convert_annotations(input_folder, output_folder, img_width, img_height)
