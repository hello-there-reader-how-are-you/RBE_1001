# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       alexandertheofilou                                           #
# 	Created:      11/23/2025, 11:09:04 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

TARGET_WALL_DISTANCE = 125 #mm
DRIVE_SPEED = 50 #RPM
DRIVE_MAX = 1.5*DRIVE_SPEED
DRIVE_MIN = 0.5*DRIVE_SPEED
Drive_PGain = 0.1*5

# Brain should be defined by default
brain=Brain()

imu = Inertial(Ports.PORT13)
imu.calibrate()

left_motor = Motor(Ports.PORT4, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)

Left_Sonar = Sonar(brain.three_wire_port.g)
Front_Sonar = Sonar(brain.three_wire_port.a)

wait(2, SECONDS)
print("Start")


def Approach_Fruitful_Tree():
    #Drive Towards Tree
    Pick_Fruit()

def Pick_Fruit():
    #code
    if succsessful:
        Drive_To_Basket()

def Drive_To_Basket():
    if failure:
        return
    Deposit_Fruit_In_Basket()

def Deposit_Fruit_In_Basket():
    pass

def clamp(low, val, high):
    return max(min(val, high), low)

#Idle:
while True:
    #Drive Fowards & Keep Dist. From wall
    daedalus_wall_dist = clamp(0, Left_Sonar.distance(MM), 300)
    print(daedalus_wall_dist-TARGET_WALL_DISTANCE)
    if (daedalus_wall_dist > TARGET_WALL_DISTANCE):
        print("FAR")
        left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Drive_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
        right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Drive_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
    else:
        print("CLOSE")
        left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Drive_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
        right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Drive_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))

    """
    #Detect Wall: T turn left
    front_wall_distance = Front_Sonar.distance(MM)
    if front_wall_distance <= 100: # MM to detect end of field
        imu.set_heading(0)
        while imu.heading() < 90: #90 Degree Turn
            right_motor.spin(FORWARD, DRIVE_SPEED)
            left_motor.spin(REVERSE, DRIVE_SPEED)
    """
    #Detect Tree
    #Detect Fruit
    pass
