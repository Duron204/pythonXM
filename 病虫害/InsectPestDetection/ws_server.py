"""
WebSocket检测服务器 - 独立文件，不修改原有代码
用于Vue前端的实时检测功能（视频、摄像头、图片）
"""
import asyncio
import json
import base64
import cv2
import numpy as np
from pathlib import Path

try:
    import websockets
except ImportError:
    print("请先安装: pip install websockets")
    exit(1)

# 导入原有的YOLO模型
from YOLOv8v5Model import YOLOv8v5Detector
from QtFusion.path import abs_path

# 加载模型
model = YOLOv8v5Detector()
model.load_model(model_path=abs_path("weights/best-yolov8n.pt", path_type="current"))

# 全局状态
current_task = None
stop_flag = False


def draw_detections(image, det_info):
    """在图像上绘制检测框和标签"""
    for info in det_info:
        bbox = info['bbox']
        if hasattr(bbox, 'tolist'):
            bbox = bbox.tolist()
        x1, y1, x2, y2 = map(int, bbox[:4])
        class_name = info['class_name']
        score = float(info['score'])

        # 绘制检测框
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        # 绘制标签背景
        label = f"{class_name} {score:.2f}"
        (label_w, label_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        cv2.rectangle(image, (x1, y1 - label_h - 6), (x1 + label_w + 6, y1), (0, 255, 0), -1)
        # 绘制标签文字
        cv2.putText(image, label, (x1 + 3, y1 - 3), cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 0, 0), 2)

    return image


async def process_frame(image, conf=0.25, iou=0.5):
    """处理单帧图像"""
    image = cv2.resize(image, (640, 640))

    # 预处理和预测
    params = {'conf': conf, 'iou': iou}
    model.set_param(params)
    pre_img = model.preprocess(image)
    pred, superimposed_img = model.predict(pre_img)

    # 后处理
    det = pred[0]
    detections = []
    if det is not None and len(det):
        det_info = model.postprocess(pred)
        for info in det_info:
            detections.append({
                'class_name': info['class_name'],
                'class_id': info['class_id'],
                'bbox': info['bbox'].tolist() if hasattr(info['bbox'], 'tolist') else info['bbox'],
                'score': float(info['score'])
            })
        # 在图像上绘制检测框
        image = draw_detections(image, det_info)

    # 编码标注后的图像为base64
    _, buffer = cv2.imencode('.jpg', image)
    img_base64 = base64.b64encode(buffer).decode('utf-8')

    return {
        'image': img_base64,
        'detections': detections,
        'inference_time': 0.1  # 简化
    }


async def handle_detection(websocket):
    """处理WebSocket连接"""
    global current_task, stop_flag

    print(f"客户端连接: {websocket.remote_address}")

    try:
        async for message in websocket:
            data = json.loads(message)
            msg_type = data.get('type')

            if msg_type == 'detect_image':
                # 图片检测 - 直接接收base64编码的图片数据
                conf = data.get('conf', 0.25)
                iou = data.get('iou', 0.5)
                image_data = data.get('image', '')

                if not image_data:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': '未提供图片数据'
                    }))
                    continue

                try:
                    # 解码base64图片
                    img_bytes = base64.b64decode(image_data)
                    nparr = np.frombuffer(img_bytes, np.uint8)
                    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                    if image is None:
                        raise ValueError("图片解码失败，不支持的图片格式")

                    # 处理图片
                    result = await process_frame(image, conf, iou)
                    result['type'] = 'image_result'
                    result['progress'] = 100

                    await websocket.send(json.dumps(result))
                except Exception as e:
                    await websocket.send(json.dumps({
                        'type': 'error',
                        'message': f'图片检测失败: {str(e)}'
                    }))

            elif msg_type == 'start_stream':
                # 开始视频/摄像头检测
                mode = data.get('mode', 'camera')
                path = data.get('path', '0')
                conf = data.get('conf', 0.25)
                iou = data.get('iou', 0.5)

                stop_flag = False
                current_task = asyncio.create_task(
                    stream_detection(websocket, mode, path, conf, iou)
                )

            elif msg_type == 'stop_stream':
                # 停止检测
                stop_flag = True
                if current_task:
                    current_task.cancel()
                    current_task = None
                await websocket.send(json.dumps({'type': 'status', 'status': 'stopped'}))

            elif msg_type == 'update_params':
                # 更新参数（简单处理）
                pass

    except websockets.exceptions.ConnectionClosed:
        print(f"客户端断开: {websocket.remote_address}")
    except Exception as e:
        print(f"错误: {e}")
    finally:
        stop_flag = True
        if current_task:
            current_task.cancel()


async def stream_detection(websocket, mode, path, conf, iou):
    """视频流检测 - 优化版"""
    global stop_flag

    # 打开视频源
    if mode == 'camera':
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(path)

    if not cap.isOpened():
        await websocket.send(json.dumps({
            'type': 'error',
            'message': f'无法打开{"摄像头" if mode == "camera" else "视频"}'
        }))
        return

    await websocket.send(json.dumps({'type': 'status', 'status': 'detecting'}))

    # 降低帧率，减少数据量
    target_fps = 10  # 降低到10fps
    frame_interval = 1.0 / target_fps

    try:
        while not stop_flag:
            ret, frame = cap.read()
            if not ret:
                break

            # 降低分辨率
            frame = cv2.resize(frame, (480, 360))

            # 处理帧（返回已标注检测框的图像）
            result = await process_frame(frame, conf, iou)
            result['type'] = 'frame'
            result['progress'] = 0

            # process_frame 已返回标注后的图像，直接使用（降低JPEG质量减少传输量）
            # 重新压缩以降低传输大小
            img_bytes = base64.b64decode(result['image'])
            nparr = np.frombuffer(img_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            _, buffer = cv2.imencode('.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 60])
            result['image'] = base64.b64encode(buffer).decode('utf-8')

            await websocket.send(json.dumps(result))
            await asyncio.sleep(frame_interval)

    except asyncio.CancelledError:
        pass
    finally:
        cap.release()
        await websocket.send(json.dumps({'type': 'detection_complete'}))


async def main():
    """启动服务器"""
    host = '127.0.0.1'
    port = 8765

    print(f"WebSocket服务器启动: ws://{host}:{port}")
    print("等待Vue前端连接...")

    # max_size=20MB 避免大图片base64数据被截断
    async with websockets.serve(handle_detection, host, port, max_size=20 * 1024 * 1024):
        await asyncio.Future()  # 永远运行


if __name__ == '__main__':
    asyncio.run(main())
