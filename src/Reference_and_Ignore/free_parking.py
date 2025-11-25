# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

Amotor = Motor(Ports.PORT13, GearSetting.RATIO_18_1, False)

Amotor.stop()

