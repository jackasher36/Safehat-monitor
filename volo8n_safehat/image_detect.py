from ultralytics import YOLO
import sys

import logging

# 设置日志级别为WARNING，屏蔽低于该级别的日志（如INFO和DEBUG）
logging.basicConfig(level=logging.WARNING)

# 如果你只想禁用特定模块的日志，可以指定该模块：
logging.getLogger('IMKClient').setLevel(logging.WARNING)# 加载训练完成的模型


model = YOLO('/Users/leojackasher/PycharmProjects/PythonProject2/runs/detect/train12/weights/best.pt')

# 从命令行获取传递的文件路径参数
image_path = sys.argv[1]  # 从命令行参数中获取图片路径

# 对整个目录中的图片进行推理
results = model(image_path, show=True, save=True)  # 推理并显示结果



# 遍历检测结果
for i, result in enumerate(results):  # 每张图片的检测结果
    print(f"图片 {i + 1}:")  # 输出图片编号
    count = 0
    for box in result.boxes:
        cls = int(box.cls.numpy()[0])  # 类别索引
        conf = float(box.conf.numpy()[0])  # 置信度
        xyxy = box.xyxy.numpy()[0]  # 边界框坐标 (x_min, y_min, x_max, y_max)

        # 判断是否是安全帽
        if cls == 2:  # 安全帽类别索引为 0
            count = count + 1
            print(f"spilt检测到未戴安全帽 - 置信度: {conf}")


    if count == 0:
        print(f"spilt未检测到未戴安全帽情况")