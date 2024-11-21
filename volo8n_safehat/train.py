from ultralytics import YOLO

model = YOLO('/Users/leojackasher/Downloads/yolov8n.pt')
model.train(data='/Users/leojackasher/PycharmProjects/PythonProject2/data/data.yaml', epochs=50, device='mps', freeze=[],batch=32,max_det=20, imgsz=320)
model.val()