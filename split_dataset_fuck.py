import os
import shutil
import random

def create_dirs(base_path, dirs):
    for dir_name in dirs:
        os.makedirs(os.path.join(base_path, dir_name), exist_ok=True)

def save_file_paths(file_paths, file_name, output_dir):
    with open(os.path.join(output_dir, file_name), 'w') as f:
        for path in file_paths:
            f.write(f"{path}\n")

def split_dataset(image_dir, label_dir, output_base_dir, train_ratio=0.7, val_ratio=0.15, seed=42):
    random.seed(seed)  # 設定隨機種子
    images = [f for f in os.listdir(image_dir) if f.endswith('.jpg')]
    random.shuffle(images)

    total_images = len(images)
    train_count = int(total_images * train_ratio)
    val_count = int(total_images * val_ratio)

    train_images = images[:train_count]
    val_images = images[train_count:train_count + val_count]
    test_images = images[train_count + val_count:]

    output_dir = os.path.join(output_base_dir, f"split_seed_{seed}")
    create_dirs(output_dir, ['train/images', 'train/labels', 'val/images', 'val/labels', 'test/images', 'test/labels'])

    def copy_files(image_list, split_name):
        for image in image_list:
            label = image.replace('.jpg', '.txt')
            shutil.copy(os.path.join(image_dir, image), os.path.join(output_dir, split_name, 'images', image))
            shutil.copy(os.path.join(label_dir, label), os.path.join(output_dir, split_name, 'labels', label))

    copy_files(train_images, 'train')
    copy_files(val_images, 'val')
    copy_files(test_images, 'test')

    # 生成 .txt 檔案
    save_file_paths([os.path.abspath(os.path.join(output_dir, 'train/images', img)) for img in train_images], 'train.txt', output_dir)
    save_file_paths([os.path.abspath(os.path.join(output_dir, 'val/images', img)) for img in val_images], 'val.txt', output_dir)
    save_file_paths([os.path.abspath(os.path.join(output_dir, 'test/images', img)) for img in test_images], 'test.txt', output_dir)

# 使用示例
image_dir = os.path.abspath('dataset/PCB/images')
label_dir = os.path.abspath('dataset/PCB/labels')
output_base_dir = os.path.abspath('dataset/PCB')
seed = 42
split_dataset(image_dir, label_dir, output_base_dir, seed=seed)
