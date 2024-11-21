from ultralytics import YOLO
import cv2
import csv
from datetime import datetime

# 加载训练完成的模型
model = YOLO('/Users/leojackasher/PycharmProjects/PythonProject2/runs/detect/train12/weights/best.pt')

# 设置类别名称
names = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

# 打开摄像头（默认摄像头为0）
cap = cv2.VideoCapture(0)

# 打开 CSV 文件用于记录事件
log_file = 'safety_event_log.csv'
with open(log_file, 'w', newline='') as file:
    writer = csv.writer(file)
    # 写入 CSV 表头
    writer.writerow(['Time', 'Class', 'Confidence', 'Position (x_min, y_min, x_max, y_max)'])

    while True:
        # 读取摄像头的每一帧
        ret, frame = cap.read()
        if not ret:
            print("无法从摄像头读取帧")
            break

        # 推理当前帧
        results = model(frame)

        # 获取推理结果
        for result in results:
            for box in result.boxes:
                cls = int(box.cls.numpy()[0])  # 类别索引
                conf = float(box.conf.numpy()[0])  # 置信度
                xyxy = box.xyxy.numpy()[0]  # 边界框坐标 (x_min, y_min, x_max, y_max)

                # 获取类别名称
                class_name = names[cls]

                # 获取当前时间
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                # 保存到 CSV 文件
                writer.writerow([current_time, class_name, f"{conf:.2f}", xyxy.tolist()])

                # 画边界框
                x_min, y_min, x_max, y_max = map(int, xyxy)
                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)

                # 在框上显示类别名称和置信度
                label = f"{class_name} {conf:.2f}"
                cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # 显示视频帧
        cv2.imshow("Frame", frame)

        # 按 "q" 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# 释放摄像头资源并关闭所有窗口
cap.release()
cv2.destroyAllWindows()