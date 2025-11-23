#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
controller_1 = Controller(PRIMARY)
arm_motor = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False)
hand_motor = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
left_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)


# wait for rotation sensor to fully initialize
wait(30, MSEC)


# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    random = brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res()
    urandom.seed(int(random))
      
# Set random seed 
initializeRandomSeed()


def play_vexcode_sound(sound_name):
    # Helper to make playing sounds from the V5 in VEXcode easier and
    # keeps the code cleaner by making it clear what is happening.
    print("VEXPlaySound:" + sound_name)
    wait(5, MSEC)

# add a small delay to make sure we don't print in the middle of the REPL header
wait(200, MSEC)
# clear the console to make sure we don't have the REPL in the console
print("\033[2J")

#endregion VEXcode Generated Robot Configuration

# ------------------------------------------
# 
# 	Project:      VEXcode Project
#	Author:       VEX
#	Created:
#	Description:  VEXcode V5 Python Project
# 
# ------------------------------------------

# Library imports
from vex import *

# define the states--------
IDLE = 0

DRIVING_FWD = 1

DRIVING_BKWD = 2

HAND_IDLE = .5

# start out---------------
current_state = IDLE
UP = 2.9
GRIP = 1.3
TARGET = 5


def reach_for(direction, target): 
    arm_motor.set_velocity(10, PERCENT)
    arm_motor.spin_for(direction, UP, TURNS, wait=True)


def grab_fruit(direction, target): 
    hand_motor.set_velocity(8, PERCENT)
    hand_motor.spin_for(direction, GRIP, TURNS, wait= False)
    

def drop_off(direction, target): 
    left_motor.set_velocity(60, RPM); 
    right_motor.set_velocity(60, RPM); 
    # Set motors spin 
    left_motor.spin_for(direction, TARGET, TURNS, wait = False) 
    right_motor.spin_for(direction, TARGET, TURNS, wait = False )


def handleL1():
    current_state = HAND_IDLE
    reach_for(FORWARD, UP)
    wait(1, SECONDS)
    if current_state == HAND_IDLE: 
        grab_fruit(FORWARD, GRIP)
    wait(5, SECONDS)
    reach_for(REVERSE, UP)
    wait(5, SECONDS)
    drop_off(REVERSE, TARGET)
    wait(5, SECONDS)
    right_motor.spin_to_position(2000, DEGREES)
    while True: 
        wait(5, SECONDS)
        grab_fruit(REVERSE, GRIP)
        wait(2, SECONDS)
        hand_motor.stop(HOLD)


    

controller_1.buttonL1.pressed(handleL1)

