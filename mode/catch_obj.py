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

    # 定義函數：找到遮罩的最遠兩個點
    def find_farthest_points(contour):
        max_distance = 0
        point1, point2 = None, None
        for i, p1 in enumerate(contour):
            for j in range(i + 1, len(contour)):
                p2 = contour[j]
                dist = np.linalg.norm(p1[0] - p2[0])  # 計算歐幾里得距離
                if dist > max_distance:
                    max_distance = dist
                    point1, point2 = p1[0], p2[0]
        return point1, point2

    # 定義函數：計算深度值的平均值，去除極值 0
    def compute_average_depth(depth_values):
        valid_depths = [d for d in depth_values if d > 0]
        if len(valid_depths) > 2:
            return np.mean(valid_depths)
        else:
            return 0

    try:
        start_time = time.time()
        collected_depths_object = []
        collected_depths_center = []
        object_world_coords = None
        angle = None

        # 畫面中心點像素座標
        screen_center = (640 // 2, 480 // 2)

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

            # 在影像中標記畫面中心點
            cv2.circle(color_image, screen_center, 5, (0, 0, 0), -1)  # 黑色點

            # 紀錄畫面中心點的深度值
            center_depth = depth_image[screen_center[1], screen_center[0]] * depth_scale
            collected_depths_center.append(center_depth)

            # 使用 YOLO 偵測物體
            results = model(color_image, verbose=False)

            farthest_point1, farthest_point2 = None, None
            object_center = None

            for result in results:
                if result.masks is not None:
                    for mask in result.masks.data:
                        mask_np = mask.cpu().numpy()
                        mask_resized = cv2.resize(mask_np, (color_image.shape[1], color_image.shape[0]), interpolation=cv2.INTER_NEAREST)

                        # 找到遮罩的輪廓
                        contours, _ = cv2.findContours((mask_resized * 255).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                        if len(contours) > 0:
                            contour = contours[0]  # 假設只處理第一個輪廓
                            farthest_point1, farthest_point2 = find_farthest_points(contour)
                            if farthest_point1 is not None and farthest_point2 is not None:
                                # 計算新的中心點
                                center_x = (farthest_point1[0] + farthest_point2[0]) // 2
                                center_y = (farthest_point1[1] + farthest_point2[1]) // 2
                                object_center = (center_x, center_y)

                                # 計算斜率與角度（修正斜率符號）
                                dx = farthest_point2[0] - farthest_point1[0]
                                dy = -(farthest_point2[1] - farthest_point1[1])

                                if dx == 0:
                                    slope = None
                                    angle = 90.0
                                else:
                                    slope = dy / dx
                                    angle = math.atan(slope) * (180 / math.pi)

                                print(f"最遠點 1: {tuple(farthest_point1)}, 最遠點 2: {tuple(farthest_point2)}")
                                print(f"斜率: {slope if slope is not None else '無法計算（垂直）'}")
                                print(f"角度: {angle:.2f} 度")

                                # 紀錄物體中心點的深度值
                                center_depth = depth_image[center_y, center_x] * depth_scale
                                collected_depths_object.append(center_depth)

                                break  # 已找到所需點，退出輪廓處理

            # 顯示影像
            if object_center is not None:
                cv2.circle(color_image, object_center, 5, (255, 0, 0), -1)  # 標記新的中心點
            cv2.imshow("Color Image", color_image)

            # 計算經過的時間
            elapsed_time = time.time() - start_time
            if elapsed_time >= 10:  # 10 秒後停止收集
                break

            # 按 'q' 鍵退出
            key = cv2.waitKey(1)
            if key == ord('q'):
                break

        # 計算物體中心點和畫面中心點的平均深度值
        average_depth_object = compute_average_depth(collected_depths_object)
        average_depth_center = compute_average_depth(collected_depths_center)

        # 計算畫面中心點世界座標
        if average_depth_center > 0:
            X_center = (screen_center[0] - ppx) * average_depth_center / (fx*2) * 1000
            Y_center = (screen_center[1] - ppy) * average_depth_center / (fy*2) * 1000
            Z_center = average_depth_center * 1000
            screen_world_coords = (X_center, Y_center, Z_center)

            print(f"畫面中心點世界座標: ({screen_world_coords[0]:.3f}, {screen_world_coords[1]:.3f}, {screen_world_coords[2]:.3f})")

        # 計算物體世界座標
        if average_depth_object > 0 and object_center is not None:
            X_obj = (object_center[0] - ppx) * average_depth_object / (fx*2) * 1000
            Y_obj = -(object_center[1] - ppy) * average_depth_object / (fy*2) * 1000
            Z_obj = average_depth_object * 1000
            object_world_coords = (X_obj, Y_obj, Z_obj)

            print(f"物體世界座標: ({object_world_coords[0]:.3f}, {object_world_coords[1]:.3f}, {object_world_coords[2]:.3f})")

            # 計算相對座標
            if screen_world_coords is not None:
                relative_coords = (
                    object_world_coords[0] - screen_world_coords[0],
                    object_world_coords[1] - screen_world_coords[1],
                    object_world_coords[2] - screen_world_coords[2]
                )
                print(f"相對座標: ({relative_coords[0]:.3f}, {relative_coords[1]:.3f}, {relative_coords[2]:.3f})")

    finally:
        # 停止相機與釋放資源
        pipeline.stop()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
