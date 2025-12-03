from vex import *

brain=Brain()

# Robot configuration code
hand_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

#def pick_fruit():
    #put in TJ's search code to have the robot find the fruit then drive up to it then add my pick code
    

def motorTourqe():
    while hand_motor.torque() < 10:  
        hand_motor.spin(FORWARD)

hand_motor.spin(FORWARD)
