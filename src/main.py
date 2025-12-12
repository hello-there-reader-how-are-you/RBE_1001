# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       alexandertheofilou                                           #
# 	Created:      11/23/2025, 11:09:04 AM                                      #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

TARGET_WALL_DISTANCE = 150 #mm Should Be 150
DRIVE_SPEED = 80 #RPM
DRIVE_MAX = 1.5*DRIVE_SPEED
DRIVE_MIN = 0.5*DRIVE_SPEED
Wall_PGain = 0.1*5
Fruit_PGain = 1
Arm_PGain = 1

# Brain should be defined by default
brain=Brain()

imu = Inertial(Ports.PORT13)
imu.calibrate()

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
hand_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
arm_motor.set_stopping(HOLD)

Left_Sonar = Sonar(brain.three_wire_port.c)
Left_Sonar.distance(MM)

Front_Sonar = Sonar(brain.three_wire_port.g)
Front_Sonar.distance(MM)

bright = Line(brain.three_wire_port.a)

X_RESOLUTION = 320
Y_RESOLUTION = 240

eye__Green = Colordesc(1, 64, 227, 108, 12, 0.91)
eye__Purple = Colordesc(2, 153, 104, 159, 24, 0.68)
eye__Orange = Colordesc(3, 244, 120, 91, 8, 0.14)

# Basket Color Detection
eye__COLOR5 = Colordesc(5, 245, 119, 195, 16, 0.47)
eye_COLORG = Colordesc(1, 64, 227, 108, 10, 0.87)
eye__COLORP = Colordesc(2, 153, 104, 159, 22, 0.62)
eye__COLORO = Colordesc(3, 244, 120, 91, 6, 0.09)
eye__Green_B = Codedesc(1, eye__COLOR5, eye_COLORG )
eye__Orange_B = Codedesc(2, eye__COLOR5, eye__COLORO)
eye__Purple_B = Codedesc(3, eye__COLOR5, eye__COLORP)

eye = AiVision(
    Ports.PORT19, 
    eye__Green, eye__Purple, eye__Orange, 
    eye__COLOR5, eye__Green_B, eye__Orange_B, eye__Purple_B, 
    AiVision.ALL_TAGS
)

wait(2, SECONDS)
print("\033[2J")
print("Start")

def clamp(low, val, high):
    return max(min(val, high), low)

def scroll(theta):
    theta = ((theta-180)**2)**0.5 - 180
    return theta

def detect_fruits():
    all_fruits = [] #[AiVisionObject]
    all_fruits.extend(eye.take_snapshot(eye__Green))
    all_fruits.extend(eye.take_snapshot(eye__Orange))
    all_fruits.extend(eye.take_snapshot(eye__Purple))
    if all_fruits:
        all_fruits.sort(key=lambda fruit: fruit.height, reverse=True) # Sorts fruit by hieght, analogus to distance
    return all_fruits

def detect_baskets(current_fruit):
    all_baskets = [] #[AiVisionObject]
    match current_fruit.id:
        case 1:
            all_baskets.extend(eye.take_snapshot(eye__Green))
        case 2:
            all_baskets.extend(eye.take_snapshot(eye__Purple))
        case 3:
            all_baskets.extend(eye.take_snapshot(eye__Orange))
    if all_baskets:
        all_baskets.sort(key=lambda fruit: fruit.height, reverse=True) # Sorts fruit by hieght, analogus to distance
    return all_baskets

def home_arm():
    arm_motor.set_max_torque(20, PERCENT)
    arm_motor.set_timeout(2, SECONDS)
    arm_motor.spin_for(FORWARD, 1.5, TURNS, True)
    arm_motor.stop()
    arm_motor.set_max_torque(100, PERCENT)

def Approach_Fruit():
    imu.set_heading(0)
    target_x = (1/2) * X_RESOLUTION
    target_y = (1/3) * Y_RESOLUTION
    while True:
        fruits = detect_fruits()
        if (fruits):
            fruit = fruits[0]
            cx = fruit.centerX
            cy = fruit.centerY
            print(cx,cy)

            left_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED - Fruit_PGain*(cx - target_x), DRIVE_MAX))
            right_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED + Fruit_PGain*(cx - target_x), DRIVE_MAX))
            print("height =" , fruit.height)
            arm_motor.spin(REVERSE, 0.5*(cy-target_y))

            if fruit.height >= 105:
                arm_motor.stop()
                left_motor.stop()
                right_motor.stop()
                print("READY TO PICK FRUIT")
                Pick_Fruit(fruit)

def Pick_Fruit(found_fruit):
    left_motor.stop()
    right_motor.stop()
    og_angle = scroll(imu.heading())

    while abs(scroll(imu.heading()) - og_angle) <= 8: # Magic Number
        print(abs(scroll(imu.heading()) - og_angle))
        left_motor.spin(FORWARD, DRIVE_SPEED)
        right_motor.spin(REVERSE, DRIVE_SPEED)
    left_motor.stop()
    right_motor.stop()

    wait(3, SECONDS)
    arm_motor.spin_for(FORWARD, 0.3, TURNS, True)
    while bright.reflectivity() < 85:
        left_motor.spin(REVERSE, DRIVE_SPEED, RPM)
        right_motor.spin(REVERSE, DRIVE_SPEED, RPM)
    left_motor.stop()
    right_motor.stop()

    hand_motor.set_max_torque(100, PERCENT)
    while hand_motor.torque() < 0.7:  
        hand_motor.spin(FORWARD)
        print("GRASPED")
    hand_motor.set_max_torque(0.2, TorqueUnits.NM)
    print(Front_Sonar.distance(MM)) # DO NOT REMOVE
    print(imu.heading())

    while (dist := Front_Sonar.distance(MM) * math.sin(math.radians(imu.heading()-180))) > TARGET_WALL_DISTANCE:
        print(dist)
        left_motor.spin_for(FORWARD, dist, TURNS, DRIVE_SPEED, RPM, False)
        right_motor.spin_for(FORWARD, dist, TURNS, DRIVE_SPEED, RPM, False)
    wall_follow(detect_baskets, found_fruit, Drive_To_Basket)

def Drive_To_Basket(fruit):
    target_x = (1/2) * X_RESOLUTION
    target_y = (2/3) * Y_RESOLUTION
    while True:
        basket = detect_baskets(fruit)
        if (basket):
            basket = basket[0]
            cx = basket.centerX
            cy = basket.centerY
            print(cx,cy)

            left_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED - Fruit_PGain*(cx - target_x), DRIVE_MAX))
            right_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED + Fruit_PGain*(cx - target_x), DRIVE_MAX))
            print("height =" , basket.height)
            arm_motor.spin(REVERSE, 0.5*(cy-target_y))

            if basket.height >= 35:
                arm_motor.stop()
                left_motor.stop()
                right_motor.stop()
                print("READY TO DEPOSIT FRUIT")
                Deposit_Fruit_In_Basket()
        
def Deposit_Fruit_In_Basket():
    arm_motor.spin_for(REVERSE, 3, TURNS, 20, RPM, True)

def wall_follow(viz = lambda: None, vargs = (), consequence = lambda: None):
    while True:
        if cargs := viz(*vargs) :
            consequence(cargs)

        #Drive Fowards & Keep Dist. From wall
        daedalus_wall_dist = clamp(0, Left_Sonar.distance(MM), 300)
        #print(daedalus_wall_dist-TARGET_WALL_DISTANCE)
        if (daedalus_wall_dist > TARGET_WALL_DISTANCE):
            print("FAR")
            left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Wall_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
            right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Wall_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
        else:
            print("CLOSE")
            left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Wall_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
            right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Wall_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))

        #Detect Wall: T turn left
        front_wall_distance = Front_Sonar.distance(MM)
        print(front_wall_distance)
        if front_wall_distance <= 400: # MM to detect end of field, Should Be 400
            print("TURNING")
            left_motor.stop()
            right_motor.stop()
            imu.set_heading(0)
            wait(2)
            print(-scroll(imu.heading()))
            while -scroll(imu.heading()) <= 20: #90 Degree Turn
                right_motor.spin(FORWARD, DRIVE_MAX)
            left_motor.spin_for(FORWARD,180, DEGREES, DRIVE_SPEED)
            right_motor.spin_for(FORWARD, 180, DEGREES, DRIVE_SPEED)
            while -scroll(imu.heading()) <= 90: #90 Degree Turn
                right_motor.spin(FORWARD, DRIVE_MAX)

home_arm()
print("Arm Homed")
arm_motor.spin_for(FORWARD, 1.2, TURNS, True)

wall_follow(detect_fruits, (), Approach_Fruit)
