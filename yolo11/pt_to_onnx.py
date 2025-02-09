import torch

# 设定模型路径
model_path = r'D:\yolo11\best-toy-20241019.pt'

# 加载YOLOv5模型，并强制重新加载最新代码
model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path, force_reload=True)

# 导出模型为ONNX格式
onnx_path = r'D:\yolo11\best-toy-20241019.onnx'
model.eval()  # 切换到评估模式
dummy_input = torch.randn(1, 3, 640, 640)  # 创建输入的dummy tensor，与YOLOv5的输入大小匹配

torch.onnx.export(model, dummy_input, onnx_path, verbose=True, opset_version=12)

print(f"模型成功导出到：{onnx_path}")
