# A basic example of commanding the robot to drive forward and backward with the press of a button.

# Library imports
from vex import *

# define the states
IDLE = 0
DRIVING_FWD = 1
PICK_UP = 2
HOMING = 3
WEIGH = 4

current_state = IDLE

brain=Brain()

left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, True)

#arm_motor.spin_to_position(POS)

ultRng = Sonar(brain.three_wire_port.c)

controller = Controller()

def home_arm():
    arm_motor.spin(FORWARD, -40)
    while True:
        brain.screen.print_at(arm_motor.torque(),x=20,y=20)
        wait(0.1, SECONDS)
        brain.screen.clear_screen()
        if arm_motor.current() > 0.3:
            arm_motor.set_position(0, DEGREES)
            break
    arm_motor.spin_to_position(186*5)


def handleLeft1Button():
    global current_state

    if(current_state == IDLE):
        print('IDLE -> FORWARDS')
        current_state = FORWARD

        while True:
            brain.screen.print(ultRng.distance(MM))
            if (ultRng.distance(MM) < 150):
                left_motor.stop()
                right_motor.stop()
                pick_up()
            left_motor.spin(FORWARD)
            right_motor.spin(FORWARD)
            brain.screen.clear_screen()

    else: # in any other state, the button acts as a kill switch
        print('? -> IDLE')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()

def pick_up():
    global current_state
    current_state=PICK_UP

    arm_motor.spin_to_position(162*5)
    weigh()

def weigh():
    global current_state
    current_state = WEIGH
    while True:
        brain.screen.print_at(arm_motor.torque()/5,x=20,y=20)
        wait(0.1, SECONDS)
        brain.screen.clear_screen()


controller.buttonL1.pressed(handleLeft1Button)


ultRng.distance(MM)
ultRng.distance(MM)
ultRng.distance(MM)

home_arm()
while True:
    wait(0.1, SECONDS)
