#region VEXcode Generated Robot Configuration
from vex import *
import random 
import math

# Brain should be defined by default
brain=Brain()
controller = Controller(PRIMARY)

# Motor and Sensor Definitions
left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
right_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
hand_motor = Motor(Ports.PORT17, GearSetting.RATIO_36_1, False)
arm_motor = Motor(Ports.PORT11, GearSetting.RATIO_36_1, False)
imu = Inertial(Ports.PORT13)
imu.calibrate()


Left_Sonar = Sonar(brain.three_wire_port.g)
Left_Sonar.distance(MM)
Front_Sonar = Sonar(brain.three_wire_port.a)
Front_Sonar.distance(MM)

# AI Vision Color Descriptions
eye__Green = Colordesc(1, 64, 227, 108, 12, 0.91)
eye__Purple = Colordesc(2, 153, 104, 159, 24, 0.68)
eye__Orange = Colordesc(3, 244, 120, 91, 8, 0.14)
eye = AiVision(Ports.PORT19, eye__Green, eye__Purple, eye__Orange, AiVision.ALL_TAGS, AiVision.ALL_AIOBJS)

# wait for rotation sensor to fully initialize
wait(30, MSEC)

# Make random actually random
def initializeRandomSeed():
    wait(100, MSEC)
    seed_value = int(brain.battery.voltage(MV) + brain.battery.current(CurrentUnits.AMP) * 100 + brain.timer.system_high_res())
    random.seed(seed_value)
      
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

                  
# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:                                                         #
# 	Created:      12/8/2025, 11:06:34 AM                                       #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #
# Library imports
from vex import *

# Begin Code 
# Define States
IDLE = 0 
SEARCHING = 1
APPROACHING = 2
GRABBING = 3
DELLIVERING = 4
RELEASING = 5

# Initialize State
current_state = IDLE

cameraInterval = 50
cameraTimer = Timer()
        
def handleButton():
    global current_state
    if(current_state == IDLE):
        print('IDLE -> SEARCHING')
        current_state = SEARCHING
        left_motor.spin(FORWARD, 20)
        right_motor.spin(FORWARD, -20)

        try:
            cameraTimer.event(cameraTimerCallback, cameraInterval)
        except NameError:
            pass
    else: 
        print('Returning to IDLE')
        current_state = IDLE
        left_motor.stop()
        right_motor.stop()

controller.buttonA.pressed(handleButton)
missed_detections = 0

def checkForLostObject():

    if (missed_detections > 20): return True 
    else : return False

def handleLostObject():
    global current_state
    if current_state == APPROACHING:
        print('APPROACHING -> SEARCHING')
        current_state = SEARCHING
        left_motor.spin(FORWARD, 30)
        right_motor.spin(FORWARD, -30)


def cameraTimerCallback():
    global current_state
    global missed_detections

    all_fruits = []
    all_fruits.extend(eye.take_snapshot(eye__Green))
    all_fruits.extend(eye.take_snapshot(eye__Orange))
    all_fruits.extend(eye.take_snapshot(eye__Purple))
    
    if all_fruits: 
        fruit_detect(all_fruits[0])
    
    else :
        missed_detections = missed_detections + 1

   
    if (current_state != IDLE):
        cameraTimer.event(cameraTimerCallback, cameraInterval)


def fruit_detect(fruit):
    global current_state
    global object_timer
    global missed_detections

   
    cx = fruit.centerX
    cy = fruit.centerY

    if fruit.id == 1:
        fruit_name = "Green"
    elif fruit.id == 2:
        fruit_name = "Purple"
    elif fruit.id == 3:
        fruit_name = "Orange"
    else:
        fruit_name = "Unknown({fruit.id})"

    
    print("Fruit detected at X:", cx, " Y:", cy, " Width:", fruit.width, " Height:", fruit.height)
    print("Fruit:", fruit_name)
    

    if(current_state == SEARCHING):
        print('SEARCHING -> APPROACHING')
        current_state = APPROACHING
    
    if current_state == APPROACHING:
       
        target_x = 160  
        error = cx - target_x  
        k_x = 0.5
        turn_effort = k_x * error 

        
        left_speed = 80 - turn_effort
        right_speed = 80 + turn_effort

        left_motor.spin(FORWARD, left_speed)
        right_motor.spin(FORWARD, right_speed)

        missed_detections = 0

 
        if abs(error) < 10 and fruit.height > 105:
            print('APPROACHING -> GRABBING')
            current_state = GRABBING
            left_motor.stop()
            right_motor.stop()


def Pick_Fruit():
    while True:
        if (fruits := detect_fruits()):
            fruit = fruits[0]
            cx = fruit.centerX
            cy = fruit.centerY




        while hand_motor.torque() < 10:  
            hand_motor.spin(FORWARD)

def Drive_To_Basket():
    if failure:
        return
    Deposit_Fruit_In_Basket()

def Deposit_Fruit_In_Basket():
    pass


#Idle:
while True:
    if (checkForLostObject()):
        handleLostObject()

    """
    #Drive Fowards & Keep Dist. From wall
    daedalus_wall_dist = clamp(0, Left_Sonar.distance(MM), 300)
    #print(daedalus_wall_dist-TARGET_WALL_DISTANCE)
    if (daedalus_wall_dist > TARGET_WALL_DISTANCE):
        #print("FAR")
        left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Wall_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
        right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Wall_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
    else:
        #print("CLOSE")
        left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Wall_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
        right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Wall_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))


    #Detect Wall: T turn left
    front_wall_distance = Front_Sonar.distance(MM)
    print(front_wall_distance)
    if front_wall_distance <= 400: # MM to detect end of field
        print("TURNING")
        left_motor.stop()
        right_motor.stop()
        imu.set_heading(0)
        wait(2)
        print(-scroll(imu.heading()))
        while -scroll(imu.heading()) <= 20: #90 Degree Turn
            right_motor.spin(FORWARD, DRIVE_MAX)
        left_motor.spin_for(FORWARD,180, DEGREES, DRIVE_SPEED)
        right_motor.spin_for(FORWARD, 180, DEGREES, DRIVE_SPEED)
        while -scroll(imu.heading()) <= 90: #90 Degree Turn
            right_motor.spin(FORWARD, DRIVE_MAX)
    """
 
    #Detect Fruit
    if (fruits := detect_fruits()):

        Approach_Fruit()
