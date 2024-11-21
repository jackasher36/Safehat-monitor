from ultralytics import YOLO

# 加载训练完成的模型
model = YOLO('/Users/leojackasher/PycharmProjects/PythonProject2/runs/detect/train6/weights/best.pt')

# 对整个目录中的图片进行推理
results = model('/Users/leojackasher/Pictures/ScreenShoot/截屏2024-11-21 04.07.40.png', show=True)  # 推理并显示结果

# 遍历检测结果
for i, result in enumerate(results):  # 每张图片的检测结果
    print(f"图片 {i + 1}:")  # 输出图片编号
    for box in result.boxes:
        cls = int(box.cls.numpy()[0])  # 类别索引
        conf = float(box.conf.numpy()[0])  # 置信度
        xyxy = box.xyxy.numpy()[0]  # 边界框坐标 (x_min, y_min, x_max, y_max)

        # 判断是否是安全帽
        if cls == 0:  # 安全帽类别索引为 0
            print(f"检测到安全帽 - 边界框: {xyxy}, 置信度: {conf}")
        else:
            print(f"检测到其他类别（类别索引: {cls}) - 边界框: {xyxy}, 置信度: {conf}")