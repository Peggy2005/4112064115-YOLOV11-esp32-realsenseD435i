from ForwardKinematics import calculate_position
from math import radians
from BusServo import BusServo
import time

# 馬達數值轉角度
def position_to_angle(position, middle_angle, flip):
    # 檢查位置數值是否合法
    if position < 0 or position > 1000:
        raise ValueError("Position out of range (0-1000).")

    # 位置數值轉角度
    if flip:
        angle = middle_angle + (1000 - position - 500) * (240 / 1000)
    else:
        angle = middle_angle + (position - 500) * (240 / 1000)
    return angle

# 初始化 BusServo
bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

# 讀取馬達數值
def read_motor_positions():
    try:
        pos_id6 = bus_servo.get_position(6)  # Base
        pos_id5 = bus_servo.get_position(5)  # Shoulder
        pos_id4 = bus_servo.get_position(4)  # Elbow
        pos_id3 = bus_servo.get_position(3)  # Wrist

        # 檢查數值範圍
        pos_id6 = max(0, min(1000, pos_id6))
        pos_id5 = max(0, min(1000, pos_id5))
        pos_id4 = max(0, min(1000, pos_id4))
        pos_id3 = max(0, min(1000, pos_id3))

        if None in (pos_id6, pos_id5, pos_id4, pos_id3):
            print("Error: Failed to read motor positions.")
            return None, None, None, None

        print("Read Motor Positions:")
        print("Base (ID=6):", pos_id6)
        print("Shoulder (ID=5):", pos_id5)
        print("Elbow (ID=4):", pos_id4)
        print("Wrist (ID=3):", pos_id3)

        return pos_id6, pos_id5, pos_id4, pos_id3

    except Exception as e:
        print("Error while reading motor positions:", e)
        return None, None, None, None

# 主程式
if __name__ == "__main__":
    while True:
        print("Press Enter to read motor positions and calculate end effector position...")
        input()  # 等待按下 Enter 鍵

        # 讀取馬達數值
        pos_id6, pos_id5, pos_id4, pos_id3 = read_motor_positions()
        if None in (pos_id6, pos_id5, pos_id4, pos_id3):
            continue  # 如果讀取失敗，跳過此迴圈

        try:
            # 轉換馬達數值為角度
            theta0 = position_to_angle(pos_id6, middle_angle=90, flip=False)
            theta1 = position_to_angle(pos_id5, middle_angle=90, flip=True)
            theta2 = position_to_angle(pos_id4, middle_angle=0, flip=False)
            theta3 = position_to_angle(pos_id3, middle_angle=0, flip=True)

            print("Converted Angles: theta0 =", theta0, "theta1 =", theta1,
                  "theta2 =", theta2, "theta3 =", theta3)

            # 呼叫 ForwardKinematics.py 的函式計算末端座標
            x, y, z = calculate_position(theta0, theta1, theta2, theta3)

            # 輸出結果
            print("End Effector Position: X =", x, ", Y =", y, ", Z =", z)

        except ValueError as ve:
            print("Invalid motor positions received:", ve)
        except Exception as e:
            print("Error:", e)

