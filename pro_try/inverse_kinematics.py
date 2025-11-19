import math
# 副程式部分 - 負責逆向運動學和角度計算
def calculate_angles(x, y, z):
    import math
    # 定義機械臂參數
    L1 = 101
    L2 = 95
    L3 = 165
    baseHeight = 65
    cubeHalfHeight = z

    # 調整 Z 去除基座高度
    z = z - baseHeight

    # 計算距離
    horizontal_length = math.sqrt(x**2 + y**2)
    total_distance = math.sqrt(horizontal_length**2 + z**2)

    # 確認目標是否在範圍內
    if total_distance > (L1 + L2 + L3):
        raise ValueError("Target is out of range")

    # 計算 theta0
    theta0 = math.atan2(y, x)

    # 使用餘弦定理計算 theta1, theta2, theta3
    distance_project_part1 = 0.17 * total_distance
    distance_project_part2 = 0.83 * total_distance

    height1 = math.sqrt(L1**2 - distance_project_part1**2)
    theta1 = 180 - math.degrees(math.acos((L1**2 + distance_project_part1**2 - height1**2) / (2 * L1 * distance_project_part1)))

    height2 = height1 + baseHeight
    height3 = height2 - cubeHalfHeight
    hyp1 = math.sqrt(height3**2 + distance_project_part2**2)
    theta3 = 180 - math.degrees(math.acos((L3**2 + L2**2 - hyp1**2) / (2 * L3 * L2)))

    theta2_sup1_angle = math.degrees(math.acos((L1**2 + height1**2 - distance_project_part1**2) / (2 * L1 * height1)))
    theta2_sup2_angle = math.degrees(math.acos((hyp1**2 + height3**2 - distance_project_part2**2) / (2 * hyp1 * height3)))
    theta2_sup3_angle = math.degrees(math.acos((L2**2 + hyp1**2 - L3**2) / (2 * L2 * hyp1)))
    theta2 = 180 - theta2_sup1_angle - theta2_sup2_angle - theta2_sup3_angle

    # 返回計算結果（以角度表示）
    return round(math.degrees(theta0), 2), round(theta1, 2), round(theta2, 2), round(theta3, 2)

