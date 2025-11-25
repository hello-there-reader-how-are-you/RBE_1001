# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       alexandertheofilou                                           #
# 	Created:      11/5/2025, 10:45:23 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

# Brain should be defined by default
brain=Brain()

imu = Inertial(Ports.PORT6)
imu.calibrate()
wait(2, SECONDS)
print("Start")

D = 1

brain=Brain()

controller = Controller()

left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)

max = 160

dt = 0.05
Y_accel = 0

PA_Gain = 100


def sense():
    global dt
    global Y_accel
    global D
    global lvel
    global rvel
    global rolling
    if D:
        Angle = math.sin(imu.heading() * 0.01745329)
    else:
        Angle = -math.sin(imu.heading() * 0.01745329)

    print(Angle)

    if (Angle >= 0):
        lvel = max + PA_Gain*Angle
        rvel = max - PA_Gain*Angle
        
    else:
        lvel = max + PA_Gain*Angle
        rvel = max - PA_Gain*Angle

    

rolling = 0

turns = 0
def g():
    global rolling
    global turns

    if turns >1 :
        left_motor.stop()
        right_motor.stop()
        while True:
            pass

    if rolling <= 20:
        rolling += 1
        print(rolling)
    else:
        turns += 1
        rolling = 0
        print("COLLISION")
        global D
        D = not D



def handleLeft1Button():
    imu.set_heading(0, DEGREES)
    while True:
        wait(20)
        sense()
        if left_motor.torque() >= 0.18:
            g()
        if D:
            left_motor.spin(FORWARD, lvel)
            right_motor.spin(FORWARD, rvel)
        else:
            left_motor.spin(FORWARD, -lvel)
            right_motor.spin(FORWARD, -rvel)


controller.buttonL1.pressed(handleLeft1Button)

while True:
    wait(1, SECONDS)
