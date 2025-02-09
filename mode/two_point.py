# 導入必要的庫
from ultralytics import YOLO
import numpy as np
import cv2

# 載入 YOLO 模型
model_path = r"D:\mode\best.pt"  # 替換為你的模型路徑
model = YOLO(model_path)

# 載入圖片
image_path = r"D:\mode\1_Color.png"  # 替換為你的圖片路徑
image = cv2.imread(image_path)

# 獲取圖片尺寸
height, width = image.shape[:2]

# 模型推論
results = model(image)

# 建立全黑背景遮罩（單通道）
mask = np.zeros((height, width, 3), dtype=np.uint8)  # 改為彩色通道，方便添加紅點

# 清單儲存名稱與中心點
object_list = []

# 處理分割結果
for result in results:
    if hasattr(result, 'masks'):  # 確保有分割遮罩
        masks = result.masks.data.cpu().numpy()  # 提取分割遮罩
        class_ids = result.boxes.cls.cpu().numpy()  # 提取類別ID
        class_names = model.names  # 提取類別名稱

        for single_mask, class_id in zip(masks, class_ids):
            # 調整分割遮罩到圖片尺寸並平滑邊緣
            resized_mask = cv2.resize(single_mask, (width, height), interpolation=cv2.INTER_LINEAR)
            resized_mask = cv2.GaussianBlur(resized_mask, (5, 5), 0)  # 使用高斯模糊平滑邊緣

            # 合併遮罩
            mask[:, :, 0] = np.maximum(mask[:, :, 0], (resized_mask * 255).astype(np.uint8))

            # 找邊界框與中心點
            contours, _ = cv2.findContours((resized_mask * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)  # 獲取邊界框
                cx, cy = x + w // 2, y + h // 2  # 計算中心點

                # 添加紅色中心點
                cv2.circle(mask, (cx, cy), radius=5, color=(0, 0, 255), thickness=-1)  # 紅色點

                # 保存名稱與中心點到清單
                object_name = class_names[int(class_id)]
                object_list.append((object_name, (cx, cy)))

# 保存結果
output_path = r"D:\mode\output_mask.png"  # 替換為你的輸出路徑
cv2.imwrite(output_path, mask)

# 輸出名稱與中心點清單
print("物件名稱與中心點清單：")
for obj in object_list:
    print(f"物件名稱: {obj[0]}, 中心點: {obj[1]}")

# 如果需要儲存清單到檔案
list_output_path = r"D:\mode\object_list.txt"  # 替換為你的清單輸出檔案
with open(list_output_path, "w") as f:
    for obj in object_list:
        f.write(f"物件名稱: {obj[0]}, 中心點: {obj[1]}\n")

print(f"完成！遮罩與紅點已保存到：{output_path}")
print(f"名稱與中心點清單已保存到：{list_output_path}")
