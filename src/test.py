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
# AI Vision Code Descriptions
eye = AiVision(Ports.PORT19, eye__Green, eye__Purple, eye__Orange, AiVision.ALL_TAGS, AiVision.ALL_AIOBJS)

wait(2, SECONDS)
print("\033[2J")

while True:
    print(imu.heading())