import os

import torch
import yaml
from ultralytics import YOLO
from QtFusion.path import abs_path

device = "0" if torch.cuda.is_available() else "cpu"

if __name__ == '__main__':
    workers = 4
    batch = 8

    data_name = "InsectPest"
    data_path = abs_path(f'datasets/{data_name}/{data_name}.yaml', path_type='current')
    unix_style_path = data_path.replace(os.sep, '/')

    directory_path = os.path.dirname(unix_style_path)
    with open(data_path, 'r') as file:
        data = yaml.load(file, Loader=yaml.FullLoader)
    if 'path' in data:
        data['path'] = directory_path
        with open(data_path, 'w') as file:
            yaml.safe_dump(data, file, sort_keys=False)

    # ========== YOLOv8s (small) 训练 ==========
    # 已存在本地 weights/yolov8s.pt，精度比 yolov8n 显著提升
    model = YOLO(abs_path('./weights/yolov8s.pt'), task='detect')
    results = model.train(
        data=data_path,
        device=device,
        workers=workers,
        imgsz=640,
        epochs=150,
        batch=batch,
        name='train_v8s_' + data_name,
        patience=30,  # early stopping，30轮不提升则自动停止
    )
    print("YOLOv8s 训练完成！")
