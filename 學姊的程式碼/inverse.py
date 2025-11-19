from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time, ustruct
#import numpy as np

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

def transform_coordinates(x1, y1, z1):
    # 定義線性變換矩陣 A 和位移向量 b
    A = [[-9.53128123, -0.00136586469],
         [0.0417681628, 6.99054572]]
    b = [16.24220161, 84.9637588]
    
    # 計算對應的 (x2, y2)
    x2 = A[0][0] * x1 + A[0][1] * y1 + b[0]
    x2 = x2*1.65
    y2 = A[1][0] * x1 + A[1][1] * y1 + b[1]
    y2 = y2*1.2
    z2 = z1
    print(x2,y2)
    # 返回轉換後的座標 (x2, y2)
    return [x2, y2, z2]

def run_action_group(BusServo, action_groups_init):
    for action in action_groups_init:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']

        BusServo.run(servo_id, position, run_time)
  
    max_time = max(action['time'] for action in action_groups_init)

    time.sleep(max_time / 1000.0)



def AngleConvert(angle, middle_angle, flip):

  # 0~240° ————> 0~1000

  p = 500 + (angle - middle_angle) * 25 / 6

  if p < 0:

    p = 0

  elif p > 1000:

    p = 1000

  if flip: return 1000 - int(p)
  #print(p)
  return int(p)
  
def ArmControl(coordinate, _time):
  angle = ArmIK.CalcAngle(X = coordinate[0], Y = coordinate[1], Z = coordinate[2])
  if angle == False:
    return False
  bus_servo.run(6, AngleConvert(angle[0] , middle_angle=90, flip=False), _time)
  bus_servo.run(5, AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
  bus_servo.run(4, AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
  bus_servo.run(3, AngleConvert(angle[3] - 1, middle_angle=-120, flip=True), _time)
  bus_servo.run(2, 500, _time)
  #bus_servo.run(1, 500, _time)
  bus_servo.run(1, 700, 1500)

  print(angle)

  return True



if __name__ == '__main__':

  while True:

    coor=[]

    coor.append(int(input("請輸入x座標: ")))

    coor.append(int(input("請輸入y座標: ")))

    coor.append(int(input("請輸入z座標: ")))



    run_action_group(bus_servo, action_groups_init)
    time.sleep_ms(100) 

    transformed_coords = transform_coordinates(coor[0], coor[1] ,coor[2])
    ArmControl(transformed_coords,2500) 
    time.sleep_ms(2500)

