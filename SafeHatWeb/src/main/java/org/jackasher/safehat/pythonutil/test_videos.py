from ultralytics import YOLO

# 加载训练完成的模型
model = YOLO('/Users/leojackasher/PycharmProjects/PythonProject2/runs/detect/train6/weights/best.pt')

# 推理视频文件
results = model('/Users/leojackasher/Download/Compressed/helmet_video-master/helmet_video/3.gif', save=True, show=True,classes=[2])  # 对视频进行推理并保存结果

# 遍历检测结果
for frame_idx, result in enumerate(results):  # 每帧的检测结果
    print(f"帧 {frame_idx + 1}:")
    for box in result.boxes:
        cls = int(box.cls.numpy()[0])  # 类别索引
        conf = float(box.conf.numpy()[0])  # 置信度
        xyxy = box.xyxy.numpy()[0]  # 边界框坐标 (x_min, y_min, x_max, y_max)

        # 判断是否是安全帽
        if cls == 0:  # 假设安全帽类别索引为 0
            print(f"检测到安全帽 - 边界框: {xyxy}, 置信度: {conf}")