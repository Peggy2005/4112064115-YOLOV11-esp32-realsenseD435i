import pyrealsense2 as rs
import numpy as np
import cv2
from ultralytics import YOLO
import time
import math

def main():
    # 初始化 RealSense 相機
    pipeline = rs.pipeline()

    # 配置相機
    config = rs.config()
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  # 深度流
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)  # 彩色流

    # 啟動管道
    pipeline.start(config)

    # 獲取相機的內參
    profile = pipeline.get_active_profile()
    depth_stream = profile.get_stream(rs.stream.depth)
    intrinsics = depth_stream.as_video_stream_profile().get_intrinsics()

    # 提取內參
    fx, fy = intrinsics.fx, intrinsics.fy
    ppx, ppy = intrinsics.ppx, intrinsics.ppy

    # 獲取深度比例
    depth_scale = profile.get_device().first_depth_sensor().get_depth_scale()

    # 初始化 YOLO 模型
    model_path = r"D:\\mode\\best.pt"  # 替換為你的模型路徑
    model = YOLO(model_path)

    # 初始化計算深度值
    center_depth_values = []  # 中心點的深度值
    object_depth_values = {}  # 儲存每個檢測點的深度值列表

    # 設定中心點
    center_pixel = (640 // 2, 480 // 2)  # 中心點像素 (x, y)

    # 判斷兩點是否接近（設定像素範圍閾值，例如 5 個像素）
    def is_close(point1, point2, threshold=5):
        return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2) <= threshold

    # 合併檢測到的相近物體點
    def merge_close_points(points, depths):
        merged_points = {}
        for i, point in enumerate(points):
            merged = False
            for merged_point in merged_points.keys():
                if is_close(point, merged_point):
                    # 合併深度值
                    merged_points[merged_point].extend(depths[i])
                    merged = True
                    break
            if not merged:
                merged_points[point] = depths[i]
        return merged_points

    # 開始時間
    start_time = time.time()
    try:
        while True:
            # 獲取幀數據
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()

            if not depth_frame or not color_frame:
                continue

            # 將幀轉為 NumPy 陣列
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            # 獲取中心點的深度值（公尺）
            center_depth = depth_image[center_pixel[1], center_pixel[0]] * depth_scale  # 單位: m
            if center_depth > 0:  # 僅記錄有效深度值
                center_depth_values.append(center_depth)

            # 使用 YOLO 偵測物體
            results = model(color_image, verbose=False)

            detected_points = []
            detected_depths = []

            for result in results:
                if result.boxes is not None:
                    bboxes = result.boxes.xyxy.cpu().numpy()
                    for bbox in bboxes:
                        xmin, ymin, xmax, ymax = map(int, bbox)
                        obj_center_x = (xmin + xmax) // 2
                        obj_center_y = (ymin + ymax) // 2

                        obj_depth = depth_image[obj_center_y, obj_center_x] * depth_scale  # 轉為公尺
                        if obj_depth > 0:
                            detected_points.append((obj_center_x, obj_center_y))
                            detected_depths.append([obj_depth])

            # 合併相近的點
            object_depth_values = merge_close_points(detected_points, detected_depths)

            # 在影像上標記中心點
            cv2.circle(color_image, center_pixel, 5, (255, 0, 0), -1)  # 藍點

            # 在影像上標記檢測到的物體點
            for obj_coords in detected_points:
                cv2.circle(color_image, obj_coords, 5, (0, 0, 255), -1)  # 紅點

            # 顯示影像
            cv2.imshow("Color Image", color_image)

            # 計算經過的時間
            elapsed_time = time.time() - start_time
            if elapsed_time >= 10:  # 10 秒後停止收集
                break

            # 按 'q' 鍵退出
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        # 計算中心點的平均深度值
        if center_depth_values:
            center_avg_depth = np.mean(center_depth_values)  # 單位: m
            print(f"中心點 10 秒內的平均深度值: {center_avg_depth:.3f} m")
        else:
            print("未檢測到中心點的有效深度值。")
            exit()

        # 計算物體點的平均深度值
        for obj_coords, depths in object_depth_values.items():
            if depths:
                object_avg_depth = np.mean(depths)  # 單位: m
                print(f"物體點 {obj_coords} 的 10 秒內平均深度值: {object_avg_depth:.3f} m")

                # 計算物體的世界座標
                X_obj = (obj_coords[0] - ppx) * object_avg_depth / (fx*2)
                Y_obj = (obj_coords[1] - ppy) * object_avg_depth / (fx*2)
                Z_obj = object_avg_depth

                print(f"物體點 {obj_coords} 世界座標 (基於平均深度, 單位: m): ({X_obj:.3f}, {Y_obj:.3f}, {Z_obj:.3f})")

        # 計算中心點的世界座標
        X_c = (center_pixel[0] - ppx) * center_avg_depth / (fx*2)
        Y_c = (center_pixel[1] - ppy) * center_avg_depth / (fx*2)
        Z_c = center_avg_depth
        center_world_coords = (X_c, Y_c, Z_c)

        X_all = (X_obj - X_c)*1000
        Y_all = -(Y_obj - Y_c)*1000
        Z_obj = Z_obj * 1000

        print(f"中心點世界座標 (基於平均深度, 單位: m): ({X_c:.3f}, {Y_c:.3f}, {Z_c:.3f})")
        print(f"相對相對世界座標 (基於平均深度, 單位: m): ({X_all:.3f}, {Y_all:.3f}, {Z_obj:.3f})")

        # 判斷是否抵達
        if abs(X_all) < 1 and abs(Y_all) < 1:
            print("成功抵達目標位置！")
        else:
            print("未抵達目標位置，20秒後重新檢測...")
            time.sleep(20)
            main()  # 重新執行程式

    finally:
        # 停止相機與釋放資源
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
