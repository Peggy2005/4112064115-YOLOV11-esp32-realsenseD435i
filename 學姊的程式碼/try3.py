from actions import action_groups
from BusServo import BusServo
import time
import math

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
        
if __name__ == '__main__':
    bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

    # Directly read the current motor positions instead of moving to a default state.
    while True:
        print("\n===== Forward Kinematics: Reading current end-effector position =====")
        input("Press Enter to read current position...")

        pos_id6, pos_id5, pos_id4, pos_id3 = read_motor_positions(bus_servo)
        if None in (pos_id6, pos_id5, pos_id4, pos_id3):
            continue

