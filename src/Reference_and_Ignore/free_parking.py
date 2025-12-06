#region VEXcode Generated Robot Configuration
from vex import *
import urandom
import math

# Brain should be defined by default
brain=Brain()

# Robot configuration code
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


# Library imports
from vex import *


# States 
IDLE = 0 
SEARCHING = 1 
APPROACHING = 2 

current_state = IDLE

cameraInterval = 50
cameraTimer = Timer()

REACH = 50

def handleButton():
    global current_state
    if current_state == IDLE:
        print('IDLE -> SEARCHING')
        current_state = SEARCHING
        left_motor.spin(FORWARD, 40)
        right_motor.spin(FORWARD, 40)
        cameraTimer.event(cameraTimerCallback, cameraInterval)
    else:
        print(' -> IDLE')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()

controller_1.buttonB.pressed(handleButton)


def cameraTimerCallback():
    global current_state

    all_fruits = []
    all_fruits.extend(eye.take_snapshot(eye__Green))
    all_fruits.extend(eye.take_snapshot(eye__Orange))
    all_fruits.extend(eye.take_snapshot(eye__Purple))

    if all_fruits:
        fruit_detect(all_fruits[0])
        current_state = APPROACHING
    else:
        if current_state = SEARCHING:
            left_motor.spin(FORWARD, 30)
            right_motor.spin(FORWARD, 30)
    cameraTimer.event(cameraTimerCallback, cameraInterval)

def fruit_detect(fruit):
    global current_state
    
    cx = fruit.centerX
    cy = fruit.centerY
    Height = fruit.height

    # Display
    brain.screen.clear_screen()
    if fruit.exists: 
        if fruit.id == 1:
            color_name = "Green"   
        elif fruit.id == 2: 
            color_name = "Purple"
        elif fruit.id == 3: 
            color_name = "Orange"
            
        brain.screen.clear_screen()
        brain.screen.set_cursor(2, 2)
        brain.screen.print("Detected:" + color_name)
        brain.screen.next_row()
        brain.screen.print("Height:", fruit.height) 
        brain.screen.next_row()
        brain.screen.print("cX:", fruit.centerX)
        brain.screen.next_row()   
        brain.screen.print("cY:", fruit.centerY)
        brain.screen.next_row()
        brain.screen.print("State", current_state)
        
        wait(100, MSEC)

       
        K_speed = 0.4 
        size_error = REACH - Height
        base_speed = K_speed * size_error
        base_speed = min(max(base_speed, -30) 30)
        target_x = 160
        K_x = 0.5
        error = cx - target_x
        turn_effort = K_x * error

    left_motor.spin(FORWARD, base_speed - turn_effort)
    right_motor.spin(FORWARD, base_speed + turn_effort) 

    if abs(size_error) < 3: 
        left_motor.stop()
        right_motor.stop()
        brain.screen.print("READY TO PICK FRUIT")
        


   




                brain.screen.clear_screen()
                brain.screen.set_cursor(2, 2)
                brain.screen.print("Detected:" + color_name)
                brain.screen.next_row()
                brain.screen.print("Height:", fruit.height) 
                brain.screen.next_row()
                brain.screen.print("cX:", fruit.centerX)
                brain.screen.next_row()   
                brain.screen.print("cY:", fruit.centerY)
                brain.screen.next_row()