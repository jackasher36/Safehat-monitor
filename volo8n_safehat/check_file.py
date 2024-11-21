from ultralytics import YOLO
import cv2
import time

# 加载训练完成的模型
model = YOLO('/Users/leojackasher/PycharmProjects/PythonProject2/runs/detect/train12/weights/best.pt')

# 设置类别名称
names = ['Hardhat', 'Mask', 'NO-Hardhat', 'NO-Mask', 'NO-Safety Vest', 'Person', 'Safety Cone', 'Safety Vest', 'machinery', 'vehicle']

# 定义警报函数
def trigger_alarm(message):
    print(f"警报：{message}")
    # 可以添加声音警报或其他通知机制

# 初始化摄像头
cap = cv2.VideoCapture(0)

# 违规记录存储文件
log_file = "violation_log.txt" + str(int(time.time()))

# 最近一次记录的时间戳
last_record_time = time.time()

# 主循环
while True:
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        print("无法从摄像头读取帧")
        break

    # 推理当前帧
    results = model(frame)

    # 获取当前时间
    current_time = time.time()

    # 获取推理结果并处理
    violations = []  # 当前帧的违规事件
    for result in results:
        for box in result.boxes:
            cls = int(box.cls.numpy()[0])  # 类别索引
            conf = float(box.conf.numpy()[0])  # 置信度
            xyxy = box.xyxy.numpy()[0]  # 边界框坐标 (x_min, y_min, x_max, y_max)

            # 获取类别名称
            class_name = names[cls]

            # 画边界框
            x_min, y_min, x_max, y_max = map(int, xyxy)
            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 0, 255), 2)

            # 在框上显示类别名称和置信度
            label = f"{class_name} {conf:.2f}"
            cv2.putText(frame, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)

            # 检测违规行为
            if class_name == 'NO-Hardhat':
                violations.append("未佩戴安全帽")

            if class_name == 'NO-Safety Vest':
                violations.append("未佩戴反光背心")

    # 每10秒记录一次违规行为到文件
    if violations and current_time - last_record_time > 10:
        last_record_time = current_time
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        with open(log_file, "a") as file:
            for violation in violations:
                file.write(f"[{timestamp}] {violation}\n")
                trigger_alarm(violation)

    # 显示当前帧
    cv2.imshow("Frame", frame)

    # 按 "q" 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源并关闭所有窗口
cap.release()
cv2.destroyAllWindows()