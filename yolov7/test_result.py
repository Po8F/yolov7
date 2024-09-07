import os
import torch
import cv2
from utils.datasets import LoadImagesAndLabels
from utils.general import non_max_suppression, scale_coords, xyxy2xywh
from utils.plots import plot_images, plot_one_box
from models.experimental import attempt_load

# 檢查是否可用 CUDA 並設置設備
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 使用正確的設備載入模型
model = attempt_load('yolov7-tiny.pt', map_location=device)
model.eval()

# 如果 CUDA 可用，將模型移動到 CUDA
if torch.cuda.is_available():
    model = model.to(device)

# 加載數據集
dataset_path = r'C:\Users\mo\PycharmProjects\yolov7\yolov7\data\coco.yaml'
assert os.path.exists(dataset_path), f"{dataset_path} 文件不存在"

# 如果 utils.datasets.LoadImagesAndLabels 不能直接讀取 coco.yaml，可以手動加載 test.txt 文件
with open(r'C:\Users\mo\PycharmProjects\yolov7\dataset\PCB\split_seed_42\test.txt', 'r') as f:
    image_paths = f.readlines()

dataset = []
for image_path in image_paths:
    image_path = image_path.strip()
    label_path = image_path.replace('images', 'labels').replace('.jpg', '.txt')
    dataset.append((image_path, label_path))

# 進行預測
for image_path, label_path in dataset:
    img = cv2.imread(image_path)
    assert img is not None, f"圖像未找到 {image_path}"

    # 將圖像轉換為 PyTorch 張量並移動到設備
    img = torch.from_numpy(img).to(device)
    img = img.permute(2, 0, 1).float() / 255.0  # 交換維度並歸一化
    img = img.unsqueeze(0)  # 添加批次維度

    # 禁用梯度計算進行推理
    with torch.no_grad():
        pred = model(img, augment=False)[0]
    pred = non_max_suppression(pred, 0.25, 0.45, classes=None, agnostic=False)

    im0s = cv2.imread(image_path)  # 加載原始圖像用於繪圖
    for i, det in enumerate(pred):
        if len(det):
            # 進行後處理
            det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
            for *xyxy, conf, cls in det:
                label = f'{model.names[int(cls)]} {conf:.2f}'
                plot_one_box(xyxy, im0s, label=label, color=[0, 255, 0], line_thickness=3)

    # 保存結果
    os.makedirs('results', exist_ok=True)
    cv2.imwrite(os.path.join('results', os.path.basename(image_path)), im0s)
