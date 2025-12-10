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

TARGET_WALL_DISTANCE = 150 #mm
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


Left_Sonar = Sonar(brain.three_wire_port.g)
Left_Sonar.distance(MM)
Front_Sonar = Sonar(brain.three_wire_port.a)
Front_Sonar.distance(MM)

X_RESOLUTION = 320
Y_RESOLUTION = 240

eye__Green = Colordesc(1, 64, 227, 108, 12, 0.91)
eye__Purple = Colordesc(2, 153, 104, 159, 24, 0.68)
eye__Orange = Colordesc(3, 244, 120, 91, 8, 0.14)
# AI Vision Code Descriptions
eye = AiVision(Ports.PORT19, eye__Green, eye__Purple, eye__Orange, AiVision.ALL_TAGS, AiVision.ALL_AIOBJS)

wait(1, SECONDS)
print("Start")


def detect_fruits():
    all_fruits = [] #[AiVisionObject]
    all_fruits.extend(eye.take_snapshot(eye__Green))
    all_fruits.extend(eye.take_snapshot(eye__Purple))
    if all_fruits:
        all_fruits.sort(key=lambda fruit: fruit.height) # Sorts fruit by hieght, analogus to distance
    return all_fruits


left_motor.spin_for(FORWARD, 3, TURNS, DRIVE_SPEED, RPM, False)
right_motor.spin_for(FORWARD, 1, TURNS, DRIVE_SPEED, RPM, True)
wait(2, SECONDS)
arm_motor.spin_for(FORWARD, 0.35, TURNS, True)