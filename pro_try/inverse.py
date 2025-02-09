from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import time
import math

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

def calculate_angles(x, y, z):
    # Define parameters
    L1 = 101
    L2 = 95
    L3 = 165
    baseHeight = 65
    cubeHalfHeight = z

    # Adjust Z to remove base height
    z = z - baseHeight

    # Calculate distances
    horizontal_length = math.sqrt(x**2 + y**2)
    total_distance = math.sqrt(horizontal_length**2 + z**2)

    # Check if within range
    if total_distance > (L1 + L2 + L3):
        raise ValueError("Target is out of range")

    # Calculate theta0
    theta0 = math.atan2(y, x)

    # Use cosine rule to calculate theta1, theta2, theta3
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

    # Return results in degrees
    return round(math.degrees(theta0), 2), round(theta1, 2), round(theta2, 2), round(theta3, 2)

def run_action_group(BusServo, action_groups_init):
    for action in action_groups_init:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']

        BusServo.run(servo_id, position, run_time)
        print("Servo ID:", servo_id, "Position:", position, "Run Time:", run_time)

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
    try:
        angles = calculate_angles(coordinate[0], coordinate[1], coordinate[2])
    except ValueError as e:
        print("Error in inverse kinematics:", e)
        return False

    positions = {
        6: AngleConvert(angles[0], middle_angle=90, flip=False),
        5: AngleConvert(angles[1] - 3, middle_angle=90, flip=True),
        4: AngleConvert(angles[2] - 2, middle_angle=0, flip=False),
        3: AngleConvert(angles[3] - 1, middle_angle=0, flip=True),
        2: 500,
        1: 700
    }

    for servo_id, position in positions.items():
        bus_servo.run(servo_id, position, _time)
        print("Servo ID:", servo_id, "Position:", position, "Time:", _time)

    print("Angles (Theta0, Theta1, Theta2, Theta3):", angles)
    return True

if __name__ == '__main__':
    while True:
        try:
            x = int(input("x: "))
            y = int(input("y: "))
            z = int(input("z: "))
            coor = [x, y, z]

            run_action_group(bus_servo, action_groups_init)
            time.sleep(0.1)

            ArmControl(coor, 2500)
            time.sleep(2.5)
        except ValueError:
            print("Invalid input. Please enter numbers only.")

