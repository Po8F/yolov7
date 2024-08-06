import os
import shutil

# 定義原始資料夾路徑和目標資料夾路徑
root_dir = 'DeepPCB-master/PCBData'
images_output_dir = '/Users/po8_fox/PycharmProjects/yolov7/dataset/PCB/images'
labels_output_dir = '/Users/po8_fox/PycharmProjects/yolov7/dataset/PCB/labels'

# 創建目標資料夾
os.makedirs(images_output_dir, exist_ok=True)
os.makedirs(labels_output_dir, exist_ok=True)

# 確認原始資料夾是否存在
if not os.path.exists(root_dir):
    print(f"根目錄 {root_dir} 不存在")
else:
    print(f"根目錄 {root_dir} 存在")

# 遍歷原始資料夾
for group_folder in os.listdir(root_dir):
    group_folder_path = os.path.join(root_dir, group_folder)
    if os.path.isdir(group_folder_path):
        print(f"檢查資料夾: {group_folder_path}")  # 調試信息

        for sub_folder in os.listdir(group_folder_path):
            sub_folder_path = os.path.join(group_folder_path, sub_folder)
            if os.path.isdir(sub_folder_path):
                print(f"檢查子資料夾: {sub_folder_path}")  # 調試信息

                # 處理 xxxx 資料夾中的 .jpg 文件
                if sub_folder.endswith(group_folder.split('group')[1]):
                    for file in os.listdir(sub_folder_path):
                        print(f"檢查文件: {file}")  # 調試信息
                        if file.endswith('.jpg') and 'test' in file:
                            source_file = os.path.join(sub_folder_path, file)
                            # 删除文件名中的 _test
                            new_file_name = file.replace('_test', '')
                            destination_file = os.path.join(images_output_dir, new_file_name)
                            print(f"複製文件: {source_file} 到 {destination_file}")  # 調試信息
                            shutil.copy(source_file, destination_file)
                            print(f"已複製文件: {source_file} 到 {destination_file}")  # 確認信息

                # 處理 xxxx_not 資料夾中的 .txt 文件
                if sub_folder.endswith(group_folder.split('group')[1] + '_not'):
                    for file in os.listdir(sub_folder_path):
                        print(f"檢查文件: {file}")  # 調試信息
                        if file.endswith('.txt'):
                            source_file = os.path.join(sub_folder_path, file)
                            destination_file = os.path.join(labels_output_dir, file)
                            print(f"複製文件: {source_file} 到 {destination_file}")  # 調試信息
                            shutil.copy(source_file, destination_file)
                            print(f"已複製文件: {source_file} 到 {destination_file}")  # 確認信息
    else:
        print(f"忽略非資料夾項目: {group_folder_path}")  # 忽略非資料夾項目
