import cv2

image_path ='C:\\Users\\mo\\PycharmProjects\\yolov7\\dataset\\PCB\\split_seed_42\\train\\images\\00041000.jpg'

image = cv2.imread(image_path)
if image is None:
    print(f"Failed to load image {image_path}")
else:
    print(f"Successfully loaded image {image_path}")
