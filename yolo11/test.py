import warnings
warnings.filterwarnings('ignore')
from ultralytics import YOLO
 
if __name__ == '__main__': 
    model = YOLO(r"D:\yolo11\dataset\yolo11m-seg.pt")
    model.train(data=r"D:\yolo11\dataset\data.yaml",
                cache=False,
                imgsz=640,
                epochs=500,  # 訓練到500個epochs
                patience=0,  # 禁用 EarlyStopping
                single_cls=False,  # 是否是單類別檢測
                batch=8,
                close_mosaic=10,
                workers=0,
                device='0',  # 使用第0號GPU
                amp=True,  # 自動混合精度訓練
                project='runs/train',
                name='exp',
                )