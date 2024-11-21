# 基于yolon8的安全帽识别

一个是Python的模型，包含了图片和视频的识别，以及调取摄像头实时识别，是否戴了安全帽，反光背心，口罩，`opencv_yolo.py`是实时摄像头检测程序，事件会被记录在`violation_log.txt`里面，`runs/detect/train12/weights/best.pt`为训练了91轮的pt文件

一个是springboot后端，可视化的前端页面，传入图片或视频，判断是否有未戴口罩行为，以命令台的方式传入参数，调用python文件进行识别，`video_detect.py`用于检测视频,`image_detect.py`用于检测图片，`index.html`为主页面

## 前端展示页面

![image-20241122001911995](https://p.ipic.vip/v4g25d.png)

## python展示页面

![image-20241122002104836](https://p.ipic.vip/fdtuad.png)