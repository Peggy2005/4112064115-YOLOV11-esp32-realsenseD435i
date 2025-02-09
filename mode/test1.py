import pyrealsense2 as rs
import numpy as np
import cv2
import time

# 配置 RealSense 管道
pipeline = rs.pipeline()

# 配置相机
config = rs.config()
config.enable_stream(rs.stream.depth)  # 启用深度流
config.enable_stream(rs.stream.color)  # 启用彩色流

# 启动管道
pipeline.start(config)

# 获取相机的内参
profile = pipeline.get_active_profile()
depth_stream = profile.get_stream(rs.stream.depth)
intrinsics = depth_stream.as_video_stream_profile().get_intrinsics()

# 固定的深度值（单位：米）
fixed_depth = 0.201  # 20.6 公分 = 0.206 米

# 指定需要计算世界坐标的像素坐标
pixel_coords = [(560, 352), (640, 360)]  # (x1, y1) 和 (x2, y2)

# 实时循环获取图像并处理
while True:
    # 获取帧数据
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    # 将深度图像转化为 NumPy 数组
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())

    # 获取并转换每个点的世界坐标
    for (x, y) in pixel_coords:
        # 使用内参将像素坐标 (x, y) 转换为相机坐标 (X, Y, Z)
        fx = intrinsics.fx  # 焦距（x方向）
        fy = intrinsics.fy  # 焦距（y方向）
        ppx = intrinsics.ppx  # 主点 x
        ppy = intrinsics.ppy  # 主点 y

        # 使用固定的深度值计算相机坐标
        X_c = (x - ppx) * fixed_depth / fx
        Y_c = (y - ppy) * fixed_depth / fy
        Z_c = fixed_depth  # Z值为固定深度

        # 输出世界坐标
        print(f"World coordinates at ({x}, {y}): ({X_c}, {Y_c}, {Z_c})")

        # 在彩色图像上绘制蓝点标记世界坐标
        cv2.circle(color_image, (x, y), 5, (255, 0, 0), -1)  # 蓝色 (255, 0, 0)

    # 显示彩色图像
    cv2.imshow("Color Image", color_image)

    # 按 'q' 键退出
    key = cv2.waitKey(1)
    if key == ord('q'):
        break

# 结束管道
pipeline.stop()
cv2.destroyAllWindows()
