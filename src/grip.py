from vex import *
from main import Pick_Fruit

brain=Brain()

# Robot configuration code
arm_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
hand_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

def move_arm():
    arm_motor.spin(FORWARD)

def motorTourqe():
    while hand_motor.torque() < 10:  
        hand_motor.spin(FORWARD)

hand_motor.spin(FORWARD)

def Deposit_Fruit_In_Basket():
    hand_motor.spin(REVERSE)
