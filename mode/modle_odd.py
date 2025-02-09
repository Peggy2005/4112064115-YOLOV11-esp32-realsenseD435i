# 导入必要的库
from ultralytics import YOLO
import onnxruntime as ort
import numpy as np
import cv2

# 使用 ONNX Runtime 加载模型
def read_model_onnx(net_path, use_cuda=False):
    providers = ['CPUExecutionProvider']
    if use_cuda:
        providers = ['CUDAExecutionProvider']
    session = ort.InferenceSession(net_path, providers=providers)
    return session

# 使用 ONNX Runtime 进行分割
def perform_segmentation_onnx(img, session, seg_mode="YOLO"):
    if seg_mode == "YOLO":
        # YOLO输入预处理
        input_blob = cv2.dnn.blobFromImage(img, 1 / 255.0, (640, 640), (0, 0, 0), swapRB=True, crop=False)
        input_name = session.get_inputs()[0].name

        # 推理
        outputs = session.run(None, {input_name: input_blob})

        # 后处理 - 生成遮罩
        masks = []
        for output in outputs:
            mask = post_process_yolo_output(output, img.shape[:2])
            masks.append(mask)
        return masks

    elif seg_mode == "UNet":
        # UNet输入预处理
        input_blob = cv2.dnn.blobFromImage(img, 1.0 / 255, (640, 640), (0, 0, 0), swapRB=True, crop=False)
        input_name = session.get_inputs()[0].name

        # 推理
        outputs = session.run(None, {input_name: input_blob})

        # 后处理 - 生成遮罩
        mask = post_process_unet_output(outputs[0], img.shape[:2])
        return [mask]

# YOLO输出的后处理
def post_process_yolo_output(output, original_shape):
    # 使用简单的阈值处理
    mask = output[0][0]  # 选择第一个通道
    mask = cv2.resize(mask, original_shape, interpolation=cv2.INTER_LINEAR)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)  # 对遮罩进行平滑处理
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)  # 使用膨胀操作
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)  # 使用腐蚀操作
    mask = (mask > 0.5).astype(np.uint8) * 255  # 根据具体模型定义阈值
    return mask

# UNet输出的后处理
def post_process_unet_output(output, original_shape):
    mask = output.argmax(axis=0)  # 假设输出是多通道，选择最大概率的类别
    mask = cv2.resize(mask, original_shape, interpolation=cv2.INTER_NEAREST)
    mask = cv2.GaussianBlur(mask, (5, 5), 0)  # 对遮罩进行平滑处理
    mask = cv2.dilate(mask, np.ones((3, 3), np.uint8), iterations=1)  # 使用膨胀操作
    mask = cv2.erode(mask, np.ones((3, 3), np.uint8), iterations=1)  # 使用腐蚀操作
    return mask * 255

# 加载您训练好的 YOLO 模型
yolo_model = YOLO(r"D:\mode\best_toy_20241109.pt")

# 读取图像并应用分割
model_path = r"D:\mode\best-toy-20241109.onnx"  # ONNX模型路径
image_path = r"D:\mode\1_Color.png"
output_dir = r"D:\mode\1_out"

# 加载ONNX模型
session = read_model_onnx(model_path, use_cuda=True)

# 加载图像
img = cv2.imread(image_path)
if img is None:
    print(f"Error: Could not read the image from {image_path}")
    exit()

# 使用 YOLO 模型进行物体检测
yolo_results = yolo_model.predict(source=image_path, task='segment', save=False)

# 存储每个图案的红色点坐标
red_points_coordinates = []

# 获取类别名称
class_names = ['circle', 'square', 'flower', 'star', 'triangle']  # 获取类别名称

# 遍历检测结果并标记点
for result in yolo_results:
    masks = result.masks  # 获取掩码数据
    classes = result.boxes.cls.tolist() if result.boxes is not None else []  # 获取每个图案的类别标签
    if masks is not None:
        for i, mask in enumerate(masks.data):
            # 将掩码转换为 NumPy 数组
            mask_np = mask.cpu().numpy()

            # 调整掩码尺寸以匹配原始图像尺寸
            mask_resized = cv2.resize(mask_np, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_NEAREST)
            mask_resized = cv2.GaussianBlur(mask_resized, (5, 5), 0)  # 对遮罩进行平滑处理
            mask_resized = cv2.dilate(mask_resized, np.ones((3, 3), np.uint8), iterations=1)  # 使用膨胀操作
            mask_resized = cv2.erode(mask_resized, np.ones((3, 3), np.uint8), iterations=1)  # 使用腐蚀操作
            mask_rgb = cv2.merge([mask_resized * 0, mask_resized * 255, mask_resized * 0]).astype(np.uint8)

            # 找到掩码的边界框
            contours, _ = cv2.findContours((mask_resized * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if len(contours) > 0:
                # 遍历每一个轮廓
                for contour in contours:
                    # 找到轮廓中的最远的两点
                    max_distance = 0
                    point1, point2 = None, None
                    for j, p1 in enumerate(contour):
                        for k in range(j + 1, len(contour)):
                            p2 = contour[k]
                            dist = np.linalg.norm(p1[0] - p2[0])
                            if dist > max_distance:
                                max_distance = dist
                                point1, point2 = p1[0], p2[0]

                    # 在图像上标记最远的两点
                    if point1 is not None and point2 is not None:
                        cv2.circle(img, (point1[0], point1[1]), radius=5, color=(0, 0, 255), thickness=-1)
                        cv2.circle(img, (point2[0], point2[1]), radius=5, color=(0, 0, 255), thickness=-1)
                        red_points_coordinates.append((tuple(point1), tuple(point2), classes[i] if i < len(classes) else -1))

            # 叠加绿色掩码到原始图像上
            mask_rgb = cv2.merge([mask_resized * 0, mask_resized * 255, mask_resized * 0]).astype(np.uint8)
            img[mask_resized > 0] = cv2.addWeighted(img[mask_resized > 0], 0, mask_rgb[mask_resized > 0], 1, 0)

# 使用ONNX模型进行分割
onnx_masks = perform_segmentation_onnx(img, session, seg_mode="YOLO")  # 可以切换 "YOLO" 或 "UNet"

# 保存ONNX分割结果
for i, mask in enumerate(onnx_masks):
    # 将单通道遮罩转换为 3 通道
    if len(mask.shape) == 2:
        mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    else:
        mask_rgb = mask
    
    # 保存为图片
    output_path = f"{output_dir}\mask_{i}.png"
    cv2.imwrite(output_path, mask_rgb)
    print(f"Saved mask to {output_path}")

# 保存标记后的图像
output_image_path = r'D:\mode\out_1.png'
cv2.imwrite(output_image_path, img)

# 显示结果图像
cv2.imshow('Result', img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 输出每个图案的红色点坐标和类别名称
for idx, (point1, point2, cls) in enumerate(red_points_coordinates):
    class_name = class_names[int(cls)] if cls != -1 else 'unknown'
    print(f'图案 {idx + 1} ({class_name}): 点1: {point1}, 点2: {point2}') 