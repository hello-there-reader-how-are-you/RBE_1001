# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       alexandertheofilou                                           #
# 	Created:      11/23/2025, 11:09:04 AM                                      #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *
import math

TARGET_WALL_DISTANCE = 150 #mm
DRIVE_SPEED = 80 #RPM
DRIVE_MAX = 1.5*DRIVE_SPEED
DRIVE_MIN = 0.5*DRIVE_SPEED
Drive_PGain = 0.1*5

# Brain should be defined by default
brain=Brain()

imu = Inertial(Ports.PORT13)
imu.calibrate()

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)

arm_motor = Motor(Ports.PORT11, GearSetting.RATIO_18_1, False)
hand_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)

Left_Sonar = Sonar(brain.three_wire_port.g)
Left_Sonar.distance(MM)
Front_Sonar = Sonar(brain.three_wire_port.a)
Front_Sonar.distance(MM)

# AI Vision Color Descriptions
REACH = 50

eye__Green = Colordesc(1, 64, 227, 108, 10, 0.2)
eye__Purple = Colordesc(2, 153, 104, 159, 10, 0.2)
eye__Orange = Colordesc(3, 244, 120, 91, 10, 0.2)
# AI Vision Code Descriptions
eye = AiVision(Ports.PORT19, eye__Green, eye__Purple, eye__Orange, AiVision.ALL_TAGS, AiVision.ALL_AIOBJS)

<<<<<<< HEAD

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

cameraInterval = 50 #MSEC?
cameraTimer = Timer()

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

"""     
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
"""

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
            # Insert Pick_Fruit Here 
=======
wait(2, SECONDS)
print("Start")


def Approach_Fruitful_Tree():
    #Drive Towards Tree
    Pick_Fruit()
>>>>>>> 70409ac23b211ff468e94f6589f46fa293421ad5

def Pick_Fruit():
    #code
    if succsessful:
        Drive_To_Basket()

def Drive_To_Basket():
    if failure:
        return
    Deposit_Fruit_In_Basket()

def Deposit_Fruit_In_Basket():
    pass

def clamp(low, val, high):
    return max(min(val, high), low)

def scroll(theta):
    theta = ((theta-180)**2)**0.5 - 180
    return theta

def grip():
    while hand_motor.torque() < 10:  
        hand_motor.spin(FORWARD)

hand_motor.spin(FORWARD) 

def move_arm():
    if Pick_Fruit: True
    arm_motor.spin(FORWARD)




#Idle:
cameraTimer.event(cameraTimerCallback, cameraInterval)
while True:
    #Drive Fowards & Keep Dist. From wall
    daedalus_wall_dist = clamp(0, Left_Sonar.distance(MM), 300)
    #print(daedalus_wall_dist-TARGET_WALL_DISTANCE)
    if (daedalus_wall_dist > TARGET_WALL_DISTANCE):
        #print("FAR")
        left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Drive_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
        right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Drive_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
    else:
        #print("CLOSE")
        left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Drive_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))
        right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Drive_PGain*(daedalus_wall_dist-TARGET_WALL_DISTANCE), DRIVE_MAX))


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
        

    #Detect Fruit
<<<<<<< HEAD
=======
        all_fruits = []
        all_fruits.extend(eye.take_snapshot(eye__Green))
        all_fruits.extend(eye.take_snapshot(eye__Orange))
        all_fruits.extend(eye.take_snapshot(eye__Purple))

        if all_fruits:
            fruit = all_fruits[0]
            cx = fruit.centerX
            cy = fruit.centerY
            Height = fruit.height
>>>>>>> 70409ac23b211ff468e94f6589f46fa293421ad5

            # Display
            brain.screen.clear_screen()
            if fruit.exists: 
                if fruit.id == 1:
                    color_name = "Green"   
                elif fruit.id == 2: 
                    color_name = "Purple"
                elif fruit.id == 3: 
                    color_name = "Orange"
            
                K_speed = 0.4
                size_error = REACH - Height
                base_speed = K_speed * size_error
                base_speed = clamp(-30, base_speed, 30)
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
                    Pick_Fruit()
