from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
from ForwardKinematics import calculate_position
import time
import math

def run_action_group(bus_servo, action_group):
    # Execute the actions in the given action group.
    for action in action_group:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']
        bus_servo.run(servo_id, position, run_time)
        print("[Initial Action] Servo ID: " + str(servo_id) + " -> Position: " + str(position) + ", Run Time: " + str(run_time) + " ms")
    max_time = max(action['time'] for action in action_group)
    time.sleep(max_time / 1000.0)

def calculate_movement(x, y, dx, dy, theta_deg):
    theta_rad = math.radians(theta_deg)
    d = math.sqrt(dx**2 + dy**2)
    alpha = math.acos(dx / d) if d != 0 else 0
    x_new = (x + d * math.cos(theta_rad + alpha))
    y_new = (y + d * math.sin(theta_rad + alpha))
    return x_new, y_new

def position_to_angle(position, middle_angle, flip):
    # Convert a motor control value (0-1000) to an angle.
    if position < 0 or position > 1000:
        raise ValueError("Position out of range (0-1000).")
    if flip:
        angle = middle_angle + (1000 - position - 500) * (240 / 1000)
    else:
        angle = middle_angle + (position - 500) * (240 / 1000)
    return angle

def read_motor_positions(bus_servo):
    # Read motor positions for IDs 6, 5, 4, and 3.
    try:
        pos_id6 = bus_servo.get_position(6)  # Base
        pos_id5 = bus_servo.get_position(5)  # Shoulder
        pos_id4 = bus_servo.get_position(4)  # Elbow
        pos_id3 = bus_servo.get_position(3)  # Wrist

        pos_id6 = max(0, min(1000, pos_id6))
        pos_id5 = max(0, min(1000, pos_id5))
        pos_id4 = max(0, min(1000, pos_id4))
        pos_id3 = max(0, min(1000, pos_id3))

        if None in (pos_id6, pos_id5, pos_id4, pos_id3):
            print("Error: Failed to read motor positions.")
            return None, None, None, None

        print("\n[Forward Kinematics] Motor positions read:")
        print("Base (ID=6): " + str(pos_id6))
        print("Shoulder (ID=5): " + str(pos_id5))
        print("Elbow (ID=4): " + str(pos_id4))
        print("Wrist (ID=3): " + str(pos_id3))
        return pos_id6, pos_id5, pos_id4, pos_id3
    except Exception as e:
        print("Error reading motor positions: " + str(e))
        return None, None, None, None

def calculate_angles(x, y, z):
    # Compute the required joint angles (in degrees) for a target position (x, y, z)
    L1 = 101
    L2 = 95
    L3 = 165
    baseHeight = 65
    cubeHalfHeight = z

    z_adjusted = z - baseHeight
    horizontal_length = math.sqrt(x**2 + y**2)
    total_distance = math.sqrt(horizontal_length**2 + z_adjusted**2)
    if total_distance > (L1 + L2 + L3):
        raise ValueError("Target is out of range")

    theta0 = math.atan2(y, x)  # in radians

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

    return round(math.degrees(theta0), 2), round(theta1, 2), round(theta2, 2), round(theta3, 2)

def AngleConvert(angle, middle_angle, flip):
    # Convert an angle (0-240°) to a motor control value (0-1000)
    p = 500 + (angle - middle_angle) * 25 / 6
    if p < 0:
        p = 0
    elif p > 1000:
        p = 1000
    if flip:
        return 1000 - int(p)
    return int(p)

def ArmControl(target_coordinate, run_time, bus_servo):
    # Compute inverse kinematics for the target position, convert joint angles to motor control values,
    # and send commands to the motors.
    try:
        angles = calculate_angles(target_coordinate[0], target_coordinate[1], target_coordinate[2])
    except ValueError as e:
        print("Inverse kinematics calculation failed: " + str(e))
        return False

    positions = {
        6: AngleConvert(angles[0], middle_angle=90, flip=False),
        5: AngleConvert(angles[1] - 3, middle_angle=90, flip=True),
        4: AngleConvert(angles[2] - 2, middle_angle=0, flip=False),
        3: AngleConvert(angles[3] - 1, middle_angle=0, flip=True),
        2: 500,
        1: 700
    }

    print("\n[Action Info]")
    print("Planned joint angles (degrees):")
    print("Theta0: " + str(angles[0]))
    print("Theta1: " + str(angles[1]))
    print("Theta2: " + str(angles[2]))
    print("Theta3: " + str(angles[3]))
    print("Corresponding motor control values: " + str(positions))

    for servo_id, position in positions.items():
        bus_servo.run(servo_id, position, run_time)
        print("Servo ID: " + str(servo_id) + " -> Position: " + str(position) + ", Run Time: " + str(run_time) + " ms")
    return True

if __name__ == '__main__':
    bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

    # Directly read the current motor positions instead of moving to a default state.
    while True:
        print("\n===== Forward Kinematics: Reading current end-effector position =====")
        input("Press Enter to read current position...")

        pos_id6, pos_id5, pos_id4, pos_id3 = read_motor_positions(bus_servo)
        if None in (pos_id6, pos_id5, pos_id4, pos_id3):
            continue

        try:
            theta0 = position_to_angle(pos_id6, middle_angle=90, flip=False)
            theta1 = position_to_angle(pos_id5, middle_angle=90, flip=True)
            theta2 = position_to_angle(pos_id4, middle_angle=0, flip=False)
            theta3 = position_to_angle(pos_id3, middle_angle=0, flip=True)
        except Exception as e:
            print("Angle conversion error: " + str(e))
            continue

        try:
            current_x, current_y, current_z = calculate_position(theta0, theta1, theta2, theta3)
            # Invert x and y to correct the sign
            current_x = -current_x
            current_y = -current_y
            print("Current end-effector position: X = " + str(round(current_x, 2)) +
                  ", Y = " + str(round(current_y, 2)) +
                  ", Z = " + str(round(current_z, 2)))
        except Exception as e:
            print("Forward kinematics calculation error: " + str(e))
            continue

        print("\nUsing fixed relative displacement for x and y:")
        dx, dy = 50, 40  # 直接指定 x 與 y 的相對位移值
        try:
          dz = float(input("Enter Z displacement (mm): "))  # 如果也不想輸入 z，可以改成固定值，例如 dz = 2
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # 使用 calculate_movement 函式計算新的 X 與 Y 座標，
        # 其中基座角度 theta0 作為旋轉角度傳入
        target_x, target_y = calculate_movement(current_x, current_y, dx, dy, theta0)
        target_z = current_z + dz

        print("Target position: X = " + str(round(target_x, 2)) +
              ", Y = " + str(round(target_y, 2)) +
              ", Z = " + str(round(target_z, 2)))


        # Ask user to confirm the target coordinate before showing joint angles.
        confirm_target = input("Display planned joint angles for the above target coordinate? (Y to continue, N to cancel): ").strip().upper()
        if confirm_target != "Y":
            print("Action cancelled. Re-reading current position.")
            continue

        try:
            target_angles = calculate_angles(target_x, target_y, target_z)
        except ValueError as e:
            print("Inverse kinematics calculation error: " + str(e))
            continue

        print("\n[Planned Joint Angles]")
        print("Theta0: " + str(target_angles[0]) + "°")
        print("Theta1: " + str(target_angles[1]) + "°")
        print("Theta2: " + str(target_angles[2]) + "°")
        print("Theta3: " + str(target_angles[3]) + "°")

        confirmation = input("Move to the above joint angles? (Y to confirm, N to cancel): ").strip().upper()
        if confirmation == "Y":
            print("Executing inverse kinematics action...")
            ArmControl([target_x, target_y, target_z], run_time=2500, bus_servo=bus_servo)
            time.sleep(2.5)
        else:
            print("Action cancelled. Re-reading current position.")
            continue

        print("\n===== Re-checking end-effector position after action =====")
        pos_id6, pos_id5, pos_id4, pos_id3 = read_motor_positions(bus_servo)
        if None in (pos_id6, pos_id5, pos_id4, pos_id3):
            continue
        try:
            theta0 = position_to_angle(pos_id6, middle_angle=90, flip=False)
            theta1 = position_to_angle(pos_id5, middle_angle=90, flip=True)
            theta2 = position_to_angle(pos_id4, middle_angle=0, flip=False)
            theta3 = position_to_angle(pos_id3, middle_angle=0, flip=True)
            new_x, new_y, new_z = calculate_position(theta0, theta1, theta2, theta3)
            new_x = -new_x
            new_y = -new_y
            print("New end-effector position: X = " + str(round(new_x, 2)) +
                  ", Y = " + str(round(new_y, 2)) +
                  ", Z = " + str(round(new_z, 2)))
        except Exception as e:
            print("Error recalculating forward kinematics: " + str(e))




