from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time, ustruct

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

def run_action_group(BusServo, action_groups_init):
    for action in action_groups_init:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']
        
        BusServo.run(servo_id, position, run_time)
        print("Servo ID: ",servo_id, "Position: ",position," Run Time: ",run_time)

    max_time = max(action['time'] for action in action_groups_init)
    time.sleep(max_time / 1000.0)

def AngleConvert(angle, middle_angle, flip):  # 0~240° ———> 0~1000
    p = 500 + (angle - middle_angle) * 25 / 6
    if p < 0:
        p = 0
    elif p > 1000:
        p = 1000
    if flip:
        return 1000 - int(p)
    print(p)
    return int(p)

def ArmControl(coordinate, _time):
    angle = ArmIK.CalcAngle(X=coordinate[0], Y=coordinate[1], Z=coordinate[2])
    if angle == False:
        return False

    positions = {
        6: AngleConvert(angle[0], middle_angle=90, flip=False),
        5: AngleConvert(angle[1] - 3, middle_angle=90, flip=True),
        4: AngleConvert(angle[2] - 2, middle_angle=0, flip=False),
        3: AngleConvert(angle[3] - 1, middle_angle=0, flip=True),
        2: 500,
        1: 700
    }

    for servo_id, position in positions.items():
        bus_servo.run(servo_id, position, _time)
        print("Servo ID: ",servo_id," Position: ",position," Time: ",_time)

    print(angle)
    return True

if __name__ == '__main__':
    while True:
        coor = []
        coor.append(int(input("x: ")))
        coor.append(int(input("y: ")))
        coor.append(int(input("z: ")))
        
        run_action_group(bus_servo, action_groups_init)
        time.sleep(0.1)

        ArmControl(coor, 2500)
        time.sleep(2.5)


