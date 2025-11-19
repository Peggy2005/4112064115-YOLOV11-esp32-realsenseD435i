from BusServo import BusServo
import time

# 初始化 BusServo
bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

def AngleConvert(angle, middle_angle, flip):
    """
    將角度轉換為 0 ~ 1000 的馬達值。
    當角度等於 middle_angle 時，對應的值為 500。
    若 flip 為 True，則最終數值會反轉 (1000 - p)。
    """
    p = 500 + (angle - middle_angle) * 25 / 6
    if p < 0:
        p = 0
    elif p > 1000:
        p = 1000
    if flip:
        return 1000 - int(p)
    return int(p)

if __name__ == '__main__':
    while True:
        try:
            # 輸入 ID2 的角度
            angle_input = float(input("請輸入 ID2 的角度: "))
        except ValueError:
            print("請輸入有效的數字！")
            continue

        # 轉換角度為馬達值 (對於 ID2 使用 middle_angle=0, flip=True)
        motor_value = AngleConvert(angle_input, middle_angle=0, flip=True)
        print("計算得到的馬達值:", motor_value)

        # 設定移動時間 (毫秒)
        run_time = 2500

        # 發送控制指令到 ID2
        bus_servo.run(2, motor_value, run_time)
        print("Servo ID 2 移動到位置:", motor_value, "，所需時間:", run_time, "毫秒")

        # 等待動作執行完成
        time.sleep(run_time / 1000.0)

