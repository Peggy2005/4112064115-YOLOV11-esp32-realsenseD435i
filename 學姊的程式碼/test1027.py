# Enter the 2D coordinate(z axis doesn't matter) of destination.
# RobotArm will move to the point in proper angle (picking things). 
# Despite using inverse kinematics(IN) ,we only use IN to determine the main direction(ID6).
# Other servo angle we design in our own rule to garentee the accuracy. 
from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time
import math
import random

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

# #Generate random coordinate within specified constraints with filtering for large transitions
# def generate_random_coordinate(prev_coordinate=None):
    # while True:
        # x = random.randint(-299, 299)
        # y = random.randint(101, 299)
        # z = random.randint(101, 299)
        # distance = math.sqrt(x ** 2 + y ** 2)
# # 
        # #Check if within the desired range
        # if 100 < distance < 350:
            # #If previous coordinate exists, check for large jumps in coordinates
            # if prev_coordinate:
                # if abs(x - prev_coordinate[0]) > 300 or abs(y - prev_coordinate[1]) > 300 or abs(z - prev_coordinate[2]) > 300:
                    # continue  # Skip and regenerate if difference is too large
            # return [x, y, z]

# Function to run servo actions
def run_action_group(bus_servo, action_groups_init):
    for action in action_groups_init:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']
        bus_servo.run(servo_id, position, run_time)
    max_time = max(action['time'] for action in action_groups_init)
    time.sleep(max_time / 1000.0)

# Unified function for angle conversion for ID3~ID5
def angle_convert(distance,start_num,middle_angle, factor, offset,sign,constant):
    angle = start_num + factor * (distance - offset)
    print("the angle of servo is", angle)
    p = 500 + sign * (angle - middle_angle) * 25 / 6 + int(constant)
    p = max(0, min(1000, p))
    print("the p of servo is", p)
    return int(p)
    
# Unified function for angle conversion for ID6   
def AngleConvert(angle, middle_angle):
    p = 500 + (angle - middle_angle) * 25 / 6
    p = max(0, min(1000, p))
    print("the p of id6 is:", p)
    return int(p)

# Calculate distance between the object and the base of the robot arm
def calculate_distance(coordinate):
    x, y = coordinate[0], coordinate[1]
    distance = math.sqrt(x ** 2 + y ** 2)
    print("the distance between object and robot is: ", distance)
    return round(distance)
    
# Control the arm based on distance
def GoToObject(pID1, coordinate, _time):
    dist = calculate_distance(coordinate)
    angle = ArmIK.CalcAngle(X=coordinate[0], Y=coordinate[1], Z=coordinate[2])
    if angle == False:
        print("Distance out of range")
        return False, 0
    
    # define different distance range parameters combination
    # writen in dictionary
    parameters = [
        (100, 155, {"pID5": (90, 90, 0.3, 100, -1, 0), "pID4": (90, 0, -0.4, 100, 1, 0), "pID3": (90, 0, -0.16, 100, -1, 0)}),
        (155, 170, {"pID5": (120, 90, 0.2, 200, -1, 0), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.04, 100, -1, 0)}),
        (170, 190, {"pID5": (120, 90, 0.2, 200, -1, 0), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.1, 100, -1, 0)}),
        (190, 230, {"pID5": (120, 90, 0.2, 200, -1, 5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.13, 100, -1, 0)}),
        (230, 260, {"pID5": (120, 90, 0.2, 200, -1, -5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.17, 100, -1, 0)}),
        (260, 290, {"pID5": (120, 90, 0.2, 200, -1, -5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.19, 100, -1, 0)}),
        (290, 310, {"pID5": (120, 90, 0.2, 200, -1, -13), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.21, 100, -1, 0)}),

        (310, 330, {"pID5": (120, 90, 0.2, 200, -1, -30), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.26, 100, -1, 0)})
    ]
    
    # choosing the param_set base on distance between object and base of robotArm
    selected_params = None
    for min_dist, max_dist, param_set in parameters:
        if min_dist < dist <= max_dist:
            selected_params = param_set
            break
    
    if selected_params is None:
        print("Distance out of range")
        return False, 0
    
    pID5 = angle_convert(dist, *selected_params["pID5"])
    pID4 = angle_convert(dist, *selected_params["pID4"])
    pID3 = angle_convert(dist, *selected_params["pID3"])

    # control the server 
    bus_servo.run(6, AngleConvert(angle[0], middle_angle=90), _time)
    bus_servo.run(5, int(pID5), _time)
    bus_servo.run(4, int(pID4), _time)
    bus_servo.run(3, int(pID3), _time)
    bus_servo.run(2, 500, _time)
    bus_servo.run(1, int(pID1), _time)
    
    return True, pID5

def Grab(pID5_value, _time):
    #bus_servo.run(1, 200, _time)
    time.sleep_ms(1000)
    bus_servo.run(1, 600, _time)
    time.sleep_ms(1500)
    bus_servo.run(5, int(pID5_value)+50, _time)

def Release(pID5_value, _time):
    #bus_servo.run(5, int(pID5_value)+20, _time)
    time.sleep_ms(1000)
    # bus_servo.run(5, int(pID5_value), _time)
    # time.sleep_ms(1500)
    #bus_servo.run(5, int(pID5_value), _time)
    bus_servo.run(1, 200, _time)
    time.sleep_ms(1500)
    print("Initializing position")
    run_action_group(bus_servo, action_groups_init)
    time.sleep_ms(100)
        

if __name__ == '__main__':
    prev_coordinate = None
    while True:
      clear_screan = input("畫面是否淨空(T/F):")
      if  clear_screan == "F":
        
          # coordinate = generte_random_coordinate(prev_coordinate)
          # prev_coordinate = coordinate
          # print("Generated object coordinate:", coordinate)
      

        coordinate1=[]
        coordinate1.append(int(input("請輸入x座標: ")))
        coordinate1.append(int(input("請輸入y座標: ")))
        coordinate1.append(int(input("請輸入z座標: ")))
        
        time.sleep_ms(1000)
        print("Initializing position")
        run_action_group(bus_servo, action_groups_init) 
        bus_servo.run(3,400,1000)
        time.sleep_ms(2000)
        print("Going to the object:", coordinate1[0], coordinate1[1], coordinate1[2])
        success, pID5_value = GoToObject(200, coordinate1, 2500)
        
        time.sleep_ms(2500)
        Grab(pID5_value, 800)
        
        time.sleep_ms(2500)
        coordinate2=[]
        coordinate2.append(int(input("請輸入x座標: ")))
        coordinate2.append(int(input("請輸入y座標: ")))
        coordinate2.append(int(input("請輸入z座標: ")))  
          # coordinate2 = generate_random_coordinate(prev_coordinate)
          # prev_coordinate = coordinate2
          # print("Generated destination coordinate:", coordinate2)
          # 
        print("Going to the destination:", coordinate2[0], coordinate2[1], coordinate2[2])
        angle = ArmIK.CalcAngle(X=coordinate2[0], Y=coordinate2[1], Z=coordinate2[2])
        bus_servo.run(6, AngleConvert(angle[0], middle_angle=90), 1000)
        time.sleep_ms(3500)
        success, pID5_value = GoToObject(600, coordinate2, 2500)
        time.sleep_ms(2500)
        Release(pID5_value, 800)
        time.sleep_ms(2500)
      else :
        print("matching is all complete , capture another frame ")
        break





