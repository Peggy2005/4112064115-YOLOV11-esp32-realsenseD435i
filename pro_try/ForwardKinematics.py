import math

# DH 變換矩陣
def dh_transform(alpha_deg, a, d, theta_deg):
    # 將度數轉成弧度
    alpha = math.radians(alpha_deg)
    theta = math.radians(theta_deg)

    # 計算三角函數
    ca = math.cos(alpha)
    sa = math.sin(alpha)
    ct = math.cos(theta)
    st = math.sin(theta)

    # 返回 4×4 DH 矩陣
    return [
        [ct, -st,  0, a],
        [st*ca,  ct * ca,   -sa, -sa * d],
        [sa*st, ct*sa,      ca,  ca*d],
        [0,        0,       0,    1]
    ]

# 4×4 矩陣相乘
def matmul_4x4(m1, m2):
    res = [[0] * 4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            s = 0
            for k in range(4):
                s += m1[i][k] * m2[k][j]
            res[i][j] = s
    return res

# 正向運動學
def forward_kinematics(theta0, theta1, theta2, theta3, d, l1, l2, l3):
    # 計算每個轉換矩陣
    T01 = dh_transform(0, 0, d, theta0)          # ^0T1
    T12 = dh_transform(90, 0, 0, theta1)        # ^1T2
    T23 = dh_transform(0, l1, 0, theta2)        # ^2T3
    T34 = dh_transform(0, l2, 0, theta3)        # ^3T4
    T45 = dh_transform(0, l3, 0, 0)             # ^4T5

    # 連乘矩陣
    T02 = matmul_4x4(T01, T12)
    T03 = matmul_4x4(T02, T23)
    T04 = matmul_4x4(T03, T34)
    T05 = matmul_4x4(T04, T45)

    # 提取末端座標
    x = T05[0][3]
    y = T05[1][3]
    z = T05[2][3]

    return x, y, z

# 動態呼叫函式，計算末端座標
def calculate_position(theta0, theta1, theta2, theta3):
    # 固定的機械臂長度
    d = 65  # 基座到第一關節的距離
    l1 = 101  # 第一段連桿長度
    l2 = 95  # 第二段連桿長度
    l3 = 165   # 第三段連桿長度

    # 呼叫正向運動學函式
    x, y, z = forward_kinematics(theta0, theta1, theta2, theta3, d, l1, l2, l3)

    # 返回末端座標
    return x, y, z
