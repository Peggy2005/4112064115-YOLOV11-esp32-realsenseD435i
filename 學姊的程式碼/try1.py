import math
import time
from BusServo import BusServo
from ForwardKinematics import calculate_position

def AngleConvert(angle, middle_angle, flip):
    """
    Convert an angle (in degrees) to a motor control value (0-1000).
    When the angle equals middle_angle, the value is 500.
    If flip is True, the final value is reversed (1000 - p).
    """
    p = 500 + (angle - middle_angle) * 25 / 6
    if p < 0:
        p = 0
    elif p > 1000:
        p = 1000
    if flip:
        return 1000 - int(p)
    return int(p)

def calculate_movement(x, y, dx, dy, theta_deg):
    """
    Calculate new (x, y) coordinates given an initial point (x, y),
    a displacement (dx, dy), and a rotation angle theta_deg.
    """
    theta_rad = math.radians(theta_deg)
    d = math.sqrt(dx**2 + dy**2)
    alpha = math.acos(dx / d) if d != 0 else 0
    x_new = x + d * math.cos(theta_rad + alpha)
    y_new = y + d * math.sin(theta_rad + alpha)
    return x_new, y_new

def position_to_angle(position, middle_angle, flip):
    """
    Convert a motor control value (0-1000) to an angle (degrees).
    """
    if position < 0 or position > 1000:
        raise ValueError("Position out of range (0-1000).")
    if flip:
        angle = middle_angle + (1000 - position - 500) * (240 / 1000)
    else:
        angle = middle_angle + (position - 500) * (240 / 1000)
    return angle

def read_motor_positions(bus_servo):
    """
    Read motor positions for servo IDs 6, 5, 4, and 3.
    """
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
        print("Base (ID=6):", pos_id6)
        print("Shoulder (ID=5):", pos_id5)
        print("Elbow (ID=4):", pos_id4)
        print("Wrist (ID=3):", pos_id3)
        return pos_id6, pos_id5, pos_id4, pos_id3
    except Exception as e:
        print("Error reading motor positions:", str(e))
        return None, None, None, None

def calculate_angles(x, y, z):
    """
    Calculate the required joint angles (in degrees) for a target position (x, y, z).
    Adjust the following values according to your robot's geometry.
    """
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

    theta0 = math.atan2(y, x)  # Base angle (radians)

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

def ArmControl(target_coordinate, run_time, bus_servo):
    """
    Calculate inverse kinematics for the target coordinate,
    convert the joint angles to motor control values,
    and send commands to the motors except servo ID1.
    Servo ID1 will be updated separately after a delay.
    """
    try:
        angles = calculate_angles(target_coordinate[0], target_coordinate[1], target_coordinate[2])
    except ValueError as e:
        print("Inverse kinematics calculation failed:", str(e))
        return False

    positions = {
        6: AngleConvert(angles[0], middle_angle=90, flip=False),
        5: AngleConvert(angles[1] - 3, middle_angle=90, flip=True),
        4: AngleConvert(angles[2] - 2, middle_angle=0, flip=False),
        3: AngleConvert(angles[3] - 1, middle_angle=0, flip=True),
        2: 500
    }

    print("\n[Action Info]")
    print("Planned joint angles (degrees):")
    print("Theta0:", angles[0])
    print("Theta1:", angles[1])
    print("Theta2:", angles[2])
    print("Theta3:", angles[3])
    print("Corresponding motor control values (excluding servo 1):", positions)

    for servo_id, position in positions.items():
        bus_servo.run(servo_id, position, run_time)
        print("Servo ID", servo_id, "moving to position", position, "with run time", run_time, "ms")
    return True

if __name__ == '__main__':
    bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
    while True:
        # Action 1: Rotate Servo ID2
        try:
            angle_input = float(input("Enter angle for Servo ID2: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

        motor_value = AngleConvert(angle_input, middle_angle=0, flip=True)
        run_time = 2500  # milliseconds
        bus_servo.run(2, motor_value, run_time)
        print("Servo ID2 moving to position:", motor_value, "with run time:", run_time, "ms")
        time.sleep(run_time / 1000.0)
        time.sleep(3)

        # Action 2: Set Servo ID1 to 20
        bus_servo.run(1, 20, run_time)
        print("Servo ID1 moving to position: 20 with run time:", run_time, "ms")
        time.sleep(run_time / 1000.0)
        time.sleep(3)

        # Action 3: Read current position and plan movement
        print("\n===== Reading current end-effector position =====")
        input("Press Enter to continue...")
        pos_id6, pos_id5, pos_id4, pos_id3 = read_motor_positions(bus_servo)
        if None in (pos_id6, pos_id5, pos_id4, pos_id3):
            continue

        try:
            theta0 = position_to_angle(pos_id6, middle_angle=90, flip=False)
            theta1 = position_to_angle(pos_id5, middle_angle=90, flip=True)
            theta2 = position_to_angle(pos_id4, middle_angle=0, flip=False)
            theta3 = position_to_angle(pos_id3, middle_angle=0, flip=True)
        except Exception as e:
            print("Error converting motor positions to angles:", str(e))
            continue

        try:
            current_x, current_y, current_z = calculate_position(theta0, theta1, theta2, theta3)
            current_x = -current_x
            current_y = -current_y
            print("Current position: X =", round(current_x, 2),
                  "Y =", round(current_y, 2),
                  "Z =", round(current_z, 2))
        except Exception as e:
            print("Error calculating forward kinematics:", str(e))
            continue

        print("\nUsing fixed displacement: dx = 21, dy = 22")
        dx, dy = 21, 22
        try:
            dz = float(input("Enter Z displacement (mm): "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        target_x, target_y = calculate_movement(current_x, current_y, dx, dy, theta0)
        target_z = current_z + dz
        print("Target position: X =", round(target_x, 2),
              "Y =", round(target_y, 2),
              "Z =", round(target_z, 2))

        confirm_target = input("Display planned joint angles? (Y to continue, N to cancel): ").strip().upper()
        if confirm_target != "Y":
            print("Action cancelled. Restarting.")
            continue

        try:
            target_angles = calculate_angles(target_x, target_y, target_z)
        except ValueError as e:
            print("Inverse kinematics error:", str(e))
            continue

        print("\n[Planned Joint Angles]")
        print("Theta0:", target_angles[0], "°")
        print("Theta1:", target_angles[1], "°")
        print("Theta2:", target_angles[2], "°")
        print("Theta3:", target_angles[3], "°")

        confirmation = input("Move to these joint angles? (Y to confirm, N to cancel): ").strip().upper()
        if confirmation == "Y":
            print("Executing inverse kinematics action...")
            ArmControl([target_x, target_y, target_z], run_time, bus_servo)
            time.sleep(run_time / 1000.0)
            time.sleep(3)
        else:
            print("Action cancelled. Restarting.")
            continue

        # Wait 5 seconds after reaching the target before updating Servo ID1 to 700
        print("Waiting 5 seconds before updating Servo ID1 to 700...")
        time.sleep(5)
        bus_servo.run(1, 700, run_time)
        print("Servo ID1 moving to position: 700 with run time:", run_time, "ms")
        time.sleep(run_time / 1000.0)
        time.sleep(3)

        # Re-check end-effector position
        print("\n===== Re-checking end-effector position =====")
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
            print("New position: X =", round(new_x, 2),
                  "Y =", round(new_y, 2),
                  "Z =", round(new_z, 2))
        except Exception as e:
            print("Error re-calculating forward kinematics:", str(e))


