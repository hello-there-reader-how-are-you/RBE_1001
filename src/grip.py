from vex import *

brain=Brain()

# Robot configuration code
hand_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

#def pick_fruit():
    #while CameraTesting() = true:
        #
        
def motorTourqe():
    while hand_motor.torque() < 10:  
        hand_motor.spin(FORWARD)

hand_motor.spin(FORWARD)

#def move-arm():
    #put in the logic to move the arm up to where the fruit is based on TJ's find code 
