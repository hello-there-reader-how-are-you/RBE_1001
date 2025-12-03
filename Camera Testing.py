#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
# AI Classification Classroom Element IDs
class ClassroomElements:
    BLUE_BALL = 0
    GREEN_BALL = 1
    RED_BALL = 2
    BLUE_RING = 3
    GREEN_RING = 4
    RED_RING = 5
    BLUE_CUBE = 6
    GREEN_CUBE = 7
    RED_CUBE = 8
controller_1 = Controller(PRIMARY)
arm_motor = Motor(Ports.PORT21, GearSetting.RATIO_18_1, False)
hand_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
left_motor = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
# AI Vision Color Descriptions
eye__Green = Colordesc(1, 64, 227, 108, 10, 0.2)
eye__Purple = Colordesc(2, 153, 104, 159, 10, 0.2)
eye__Orange = Colordesc(3, 244, 120, 91, 10, 0.2)
# AI Vision Code Descriptions
eye = AiVision(Ports.PORT19, eye__Green, eye__Purple, eye__Orange, AiVision.ALL_TAGS, AiVision.ALL_AIOBJS)


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

# Begin project code

# States 
IDLE = 0 
SEARCHING = 1 
APPROACHING = 2 

current_state = IDLE

cameraInterval = 50
cameraTimer = Timer()

TOO_CLOSE_HEIGHT = 150
STOP_HEIGHT = 25
APPROACH_HEIGHT = 60


# ---------------------------
def handleButton():
    global current_state
    if current_state == IDLE:
        print('IDLE -> SEARCHING')
        current_state = SEARCHING
        left_motor.spin(FORWARD)
        right_motor.spin(FORWARD)
        cameraTimer.event(cameraTimerCallback, cameraInterval)
    else:
        print(' -> IDLE')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()

controller_1.buttonB.pressed(handleButton)

# ---------------------------
def cameraTimerCallback():
    global current_state

    all_fruits = []
    all_fruits.extend(eye.take_snapshot(eye__Green))
    all_fruits.extend(eye.take_snapshot(eye__Orange))
    all_fruits.extend(eye.take_snapshot(eye__Purple))

    if all_fruits:
        fruit_detect(all_fruits[0])
    else:
        if current_state == SEARCHING:
            left_motor.spin(REVERSE, 30)
            right_motor.spin(FORWARD, 30)

    if current_state != IDLE:
        cameraTimer.event(cameraTimerCallback, cameraInterval)


def fruit_detect(fruit):
    global current_state

    cx = fruit.centerX
    cy = fruit.centerY
    Height = fruit.height


    # Display

    if fruit.exists: 

        if fruit.id == 1:
            color_name = "Green"   


        elif fruit.id == 2: 
            color_name = "Purple"

        elif fruit.id == 3: 
            color_name = "Orange"
            
        brain.screen.set_cursor(2, 2)
        brain.screen.print("Detected:" + color_name)
        brain.screen.next_row()
        brain.screen.print("Height:", fruit.height) 
        brain.screen.next_row()
        brain.screen.print("cX:", fruit.centerX)
        brain.screen.next_row()   
        brain.screen.print("cY:", fruit.centerY)
        wait(2, SECONDS)
        brain.screen.clear_screen()

    else:
        brain.screen.print("Maybe Tree -> avoid")
        if cx < 160:
            left_motor.spin(FORWARD, 15)
            right_motor.spin(REVERSE, 15)
        else:
            left_motor.spin(REVERSE, 15)
            right_motor.spin(FORWARD, 15)
        return

    # Distance control
    if STOP_HEIGHT <= Height < TOO_CLOSE_HEIGHT:
        left_motor.stop()
        right_motor.stop()
        return

    if Height >= TOO_CLOSE_HEIGHT:
        left_motor.spin_for(FORWARD, 20)
        right_motor.spin_for(FORWARD, 20)
        return

    # Steering
    target_x = 160
    K_x = 0.5
    error = cx - target_x
    turn_effort = K_x * error

    base_speed = 60 if Height < APPROACH_HEIGHT else 20

    left_motor.spin(REVERSE, base_speed - turn_effort)
    right_motor.spin(REVERSE, base_speed + turn_effort)

    # Update state
    if current_state == SEARCHING:
        current_state = APPROACHING
