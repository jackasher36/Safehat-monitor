from ultralytics import YOLO
import sys

# 加载训练完成的模型
model = YOLO('/Users/leojackasher/PycharmProjects/PythonProject2/runs/detect/train12/weights/best.pt')

video_path = sys.argv[1]  # 从命令行参数中获取视频路径

# 推理视频文件
results = model(video_path, save=True, show=True, classes=[2])  # 对视频进行推理，关注类别 2（未戴安全帽）

# 假设视频帧率是固定的，可以从结果中提取帧率
fps = results.fps if hasattr(results, 'fps') else 30  # 默认帧率为 30

# 遍历检测结果
no_helmet_times = []  # 存储未戴安全帽的时间点
for frame_idx, result in enumerate(results):  # 每帧的检测结果
    for box in result.boxes:
        cls = int(box.cls.numpy()[0])  # 类别索引
        conf = float(box.conf.numpy()[0])  # 置信度

        # 判断是否是未戴安全帽
        if cls == 2:  # 假设未戴安全帽类别索引为 2
            # 计算时间点 (帧索引 / 帧率)
            time_in_seconds = frame_idx / fps
            no_helmet_times.append(time_in_seconds)
            print(f"检测到未戴安全帽 - 置信度: {conf}, 时间: {time_in_seconds:.2f} 秒")

# 打印结果
if no_helmet_times:
    print("\nspilt未戴安全帽时间点:")
    for t in no_helmet_times:
        print(f"{t:.2f} 秒")
else:
    print("\nspilt未检测到未戴安全帽的情况。")