from os import urandom
from vex import *
import math
from Pick import handleL1

brain=Brain()
controller_1 = Controller(PRIMARY)

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)

left_motor.spin(FORWARD)
right_motor.spin(FORWARD)

#controller_1.buttonL1.pressed(handleL1)