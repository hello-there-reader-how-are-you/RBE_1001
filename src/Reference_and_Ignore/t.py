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

brain=Brain()


left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)


left_motor.spin_for(FORWARD, 1, TURNS, True)
wait(2, SECONDS)
right_motor.spin_for(FORWARD, 1, TURNS, True)

print("DONE")