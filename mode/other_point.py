import pyrealsense2 as rs
import cv2
import numpy as np
from ultralytics import YOLO

# 初始化 RealSense 相機
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
pipeline.start(config)

# 載入 YOLO 模型
model_path = r"D:\mode\best_box_20250206.pt"  # 替換為你的模型路徑
model = YOLO(model_path)

try:
    while True:
        # 獲取彩色影像流
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # 將彩色影像轉為 NumPy 陣列
        color_image = np.asanyarray(color_frame.get_data())
        height, width = color_image.shape[:2]

        # 計算藍點（影像中心點）座標
        center_x, center_y = width // 2, height // 2
        cv2.circle(color_image, (center_x, center_y), radius=5, color=(255, 0, 0), thickness=-1)

        # 使用 YOLO 模型檢測物件
        results = model(color_image)

        # 儲存藍點座標與紅點相關資訊
        blue_point = (center_x, center_y)
        red_points = []  # 紅點列表

        for result in results:
            if result.boxes is not None:
                bboxes = result.boxes.xyxy.cpu().numpy()  # 提取邊界框 (xmin, ymin, xmax, ymax)
                class_ids = result.boxes.cls.cpu().numpy()  # 類別 ID

                for bbox in bboxes:
                    # 計算邊界框的中心點
                    xmin, ymin, xmax, ymax = map(int, bbox)
                    obj_center_x, obj_center_y = (xmin + xmax) // 2, (ymin + ymax) // 2

                    # 在影像上標記紅點
                    cv2.circle(color_image, (obj_center_x, obj_center_y), radius=5, color=(0, 0, 255), thickness=-1)

                    # 計算紅點相對於藍點的相對像素座標
                    relative_position = (obj_center_x - center_x, obj_center_y - center_y)

                    # 將紅點資訊加入列表
                    red_points.append({
                        "紅點座標": (obj_center_x, obj_center_y),
                        "相對藍點座標": relative_position
                    })

        # 顯示處理後的影像
        cv2.imshow("YOLO Detection", color_image)

        # 輸出藍點與紅點資訊
        print(f"藍點座標: {blue_point}")
        for idx, red_point in enumerate(red_points):
            print(f"物件 {idx + 1}: 紅點座標: {red_point['紅點座標']}, 相對藍點座標: {red_point['相對藍點座標']}")

        # 按 'q' 鍵退出
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

finally:
    # 停止相機與釋放資源
    pipeline.stop()
    cv2.destroyAllWindows()