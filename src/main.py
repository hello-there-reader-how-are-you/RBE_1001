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

imu = Inertial(Ports.PORT20)
imu.calibrate()

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
hand_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT11, GearSetting.RATIO_36_1, False)
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
# AI Vision Code Descriptions
eye = AiVision(Ports.PORT19, eye__Green, eye__Purple, eye__Orange, AiVision.ALL_TAGS, AiVision.ALL_AIOBJS)

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

def Approach_Fruit():
    arm_motor.set_max_torque(100, PERCENT)
    imu.set_heading(0)
    target_x = (1/2) * X_RESOLUTION
    target_y = (1/3) * Y_RESOLUTION
    max_height = 0
    while True:
        print(max_height)
        fruits = detect_fruits()
        if (fruits):
            fruit = fruits[0]
            cx = fruit.centerX
            cy = fruit.centerY
            #print(cx,cy)

            left_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED - Fruit_PGain*(cx - target_x), DRIVE_MAX)) #May be Flipped
            right_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED + Fruit_PGain*(cx - target_x), DRIVE_MAX)) #May be Flipped
            print("height =" , fruit.height)
            arm_motor.spin(REVERSE, 0.5*(cy-target_y))
            max_height = max(fruit.height, max_height)

        if max_height >= 100:
            arm_motor.stop()
            left_motor.stop()
            right_motor.stop()
            print("READY TO PICK FRUIT")
            while True:
                wait(1, SECONDS)
            #Pick_Fruit()


def Pick_Fruit():
    global HAVE_FRUIT
    left_motor.stop()
    right_motor.stop()
    og_angle = imu.heading()

    while imu.heading() > og_angle - 5: # Magic Number
        left_motor.spin(FORWARD, DRIVE_SPEED)
        right_motor.spin(FORWARD, DRIVE_SPEED)
        

    #left_motor.spin_for(FORWARD, 2, TURNS, DRIVE_SPEED, RPM, False)
    #right_motor.spin_for(FORWARD, 1, TURNS, DRIVE_SPEED, RPM, True)
    wait(3, SECONDS)
    arm_motor.spin_for(FORWARD, 0.2, TURNS, True)


    while bright.reflectivity() < 85:
        left_motor.spin(REVERSE, DRIVE_SPEED, RPM)
        right_motor.spin(REVERSE, DRIVE_SPEED, RPM)
    left_motor.stop()
    right_motor.stop()

    hand_motor.set_max_torque(100, PERCENT)
    while hand_motor.torque() < 0.7:  
        hand_motor.spin(FORWARD)
        print("GRASPING")
    hand_motor.set_max_torque(0.2, TorqueUnits.NM)
    HAVE_FRUIT = True
    print(Front_Sonar.distance(MM)) # DO NOT REMOVE
    print(imu.heading())

    while (dist := Front_Sonar.distance(MM) * math.sin(math.radians(imu.heading()-180))) > daedalus_wall_dist:
        print(dist)
        left_motor.spin_for(FORWARD, dist, TURNS, DRIVE_SPEED, RPM, False)
        right_motor.spin_for(FORWARD, dist, TURNS, DRIVE_SPEED, RPM, False)
    return


def Drive_To_Basket():
    #CODE NEEDED!!!!!!!!!!!
    pass
    Deposit_Fruit_In_Basket()

def Deposit_Fruit_In_Basket():
    arm_motor.spin_for(REVERSE, 3, TURNS, 20, RPM, True)
    while True:
        wait(1, SECONDS)


while arm_motor.torque() <= 1:
    arm_motor.spin(REVERSE)
arm_motor.stop()
print("Arm Homed")

arm_motor.set_max_torque(100, PERCENT)
arm_motor.spin_for(FORWARD, 1.2, TURNS, True)
HAVE_FRUIT = False
#Idle:
while True:
    #Detect Fruit
    if not HAVE_FRUIT:
        if (fruits := detect_fruits()):
            print("DETECTED A FRUIT")
            Approach_Fruit()
    if HAVE_FRUIT:
        Drive_To_Basket()
        
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
    if front_wall_distance <= -10: # MM to detect end of field, Should Be 400
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


