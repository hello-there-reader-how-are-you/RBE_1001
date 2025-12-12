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

CURRENT_FRUIT = None
HAVE_FRUIT = False

TARGET_WALL_DISTANCE = 150 #mm Should Be 150
DRIVE_SPEED = 80 #RPM
DRIVE_MAX = 1.5*DRIVE_SPEED
DRIVE_MIN = 0.5*DRIVE_SPEED
Wall_PGain = 0.1*5
Fruit_PGain = 1
Arm_PGain = 1

# Brain should be defined by default
brain=Brain()

imu = Inertial(Ports.PORT20)
imu.calibrate()

left_motor = Motor(Ports.PORT2, GearSetting.RATIO_18_1, True)
right_motor = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
hand_motor = Motor(Ports.PORT17, GearSetting.RATIO_18_1, False)
arm_motor = Motor(Ports.PORT11, GearSetting.RATIO_36_1, False)
arm_motor.set_stopping(HOLD)

Left_Sonar = Sonar(brain.three_wire_port.c)
Left_Sonar.distance(MM)

Front_Sonar = Sonar(brain.three_wire_port.g)
Front_Sonar.distance(MM)

bright = Line(brain.three_wire_port.a)

X_RESOLUTION = 320
Y_RESOLUTION = 240

eye__Green = Colordesc(1, 64, 227, 108, 12, 0.91)
eye__Purple = Colordesc(2, 153, 104, 159, 24, 0.68)
eye__Orange = Colordesc(3, 244, 120, 91, 8, 0.14)

# Basket Color Detection
eye__COLOR5 = Colordesc(5, 245, 119, 195, 16, 0.47)
eye_COLORG = Colordesc(1, 64, 227, 108, 10, 0.87)
eye__COLORP = Colordesc(2, 153, 104, 159, 22, 0.62)
eye__COLORO = Colordesc(3, 244, 120, 91, 6, 0.09)
eye__Green_B = Codedesc(1, eye__COLOR5, eye_COLORG )
eye__Orange_B = Codedesc(2, eye__COLOR5, eye__COLORO)
eye__Purple_B = Codedesc(3, eye__COLOR5, eye__COLORP)

# AI Vision sensor
eye = AiVision(
    Ports.PORT19, 
    eye__Green, eye__Purple, eye__Orange, 
    eye__COLOR5, eye__Green_B, eye__Orange_B, eye__Purple_B, 
    AiVision.ALL_TAGS
)

wait(2, SECONDS)
print("\033[2J")
print("Start")
left_motor.set_max_torque(100, PERCENT)
right_motor.set_max_torque(100, PERCENT)

def clamp(low, val, high):
    return max(min(val, high), low)

def scroll(theta):
    theta = ((theta-180)**2)**0.5 - 180
    return theta

def detect_fruits():
    all_fruits = [] #[AiVisionObject]
    all_fruits.extend(eye.take_snapshot(eye__Green))
    all_fruits.extend(eye.take_snapshot(eye__Orange))
    all_fruits.extend(eye.take_snapshot(eye__Purple))
    all_fruits = [obj for obj in all_fruits if obj.id in [eye__Green.id, eye__Orange.id, eye__Purple.id]]
    if all_fruits:
        all_fruits.sort(key=lambda fruit: fruit.height, reverse=True) # Sorts fruit by hieght, analogus to distance
    return all_fruits

def Approach_Fruit():
    arm_motor.set_max_torque(100, PERCENT)
    imu.set_heading(0)
    target_x = (1/2) * X_RESOLUTION
    target_y = (1/3) * Y_RESOLUTION
    max_height = 0
    while True:
        #print(max_height)
        fruits = detect_fruits()
        if (fruits):
            fruit = fruits[0]
            cx = fruit.centerX
            cy = fruit.centerY
            #print(cx,cy)
            global CURRENT_FRUIT
            if fruit.id == 1:
                CURRENT_FRUIT = "green"
            elif fruit.id == 2:
                CURRENT_FRUIT = "purple"
            elif fruit.id == 3:
                CURRENT_FRUIT = "orange"
            else:
                CURRENT_FRUIT = "unknown"

            print ("Detected fruit:", CURRENT_FRUIT)
            wait(50, MSEC)
            

            left_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED - Fruit_PGain*(cx - target_x), DRIVE_MAX)) #May be Flipped
            right_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED + Fruit_PGain*(cx - target_x), DRIVE_MAX)) #May be Flipped
            #print("height =" , fruit.height)
           
            arm_motor.spin(REVERSE, 0.5*(cy-target_y))
            max_height = max(fruit.height, max_height)

        if max_height >= 110:
            arm_motor.stop()
            left_motor.stop()
            right_motor.stop()
            print("READY TO PICK FRUIT")
            wait(50, MSEC)
            Pick_Fruit()
            break


def Pick_Fruit():
    global HAVE_FRUIT, CURRENT_FRUIT
    left_motor.stop()
    right_motor.stop()
    og_angle = scroll(imu.heading())

    while abs(scroll(imu.heading()) - og_angle) <= 8: # Magic Number
        #print(abs(scroll(imu.heading()) - og_angle))
        left_motor.spin(FORWARD, DRIVE_SPEED)
        right_motor.spin(REVERSE, DRIVE_SPEED)
        print("TURN")
    left_motor.stop()
    right_motor.stop()

    #left_motor.spin_for(FORWARD, 2, TURNS, DRIVE_SPEED, RPM, False)
    #right_motor.spin_for(FORWARD, 1, TURNS, DRIVE_SPEED, RPM, True)
    wait(3, SECONDS)
    arm_motor.spin_for(FORWARD, 0.3, TURNS, True)

    while bright.reflectivity() < 80:
        left_motor.spin(REVERSE, 30, RPM)
        right_motor.spin(REVERSE, 30, RPM)
        print ("STOP")
    left_motor.stop()
    right_motor.stop()

    hand_motor.set_max_torque(100, PERCENT)
    while hand_motor.torque() < 0.7:  
        hand_motor.spin(FORWARD)
        print("GRASPING")
    hand_motor.set_max_torque(0.7, TorqueUnits.NM)
    print("Thanks")
    HAVE_FRUIT = True
    if HAVE_FRUIT: 
        print("HAVE FRUIT: ", CURRENT_FRUIT)
        wait(200, MSEC)
        arm_motor.spin_for(REVERSE, 0.6, TURNS, True) #<---- Have it to go back all the way down (HOME)
        print("HOME")
        #print(Front_Sonar.distance(MM)) # DO NOT REMOVE
        #print(imu.heading())
        #while (dist := Front_Sonar.distance(MM) * math.sin(math.radians(imu.heading()-180))) > 50:
           # print(dist)
        left_motor.spin_for(FORWARD, 0.1, TURNS, DRIVE_SPEED, RPM, False)
        right_motor.spin_for(FORWARD, 0.1, TURNS, DRIVE_SPEED, RPM, False)
        print("Lets GO")

def detect_basket(CURRENT_FRUIT):
    baskets = []
    baskets.extend(eye.take_snapshot(eye__Green_B))
    baskets.extend(eye.take_snapshot(eye__Orange_B))
    baskets.extend(eye.take_snapshot(eye__Purple_B))

    if CURRENT_FRUIT == "green":
        tag = eye__Green_B
    elif CURRENT_FRUIT == "orange":
        tag = eye__Orange_B
    elif CURRENT_FRUIT == "purple":
        tag = eye__Purple_B
    else:
        return None
    print("Searching for basket of color:", CURRENT_FRUIT)
    
    matching_baskets = [b for b in baskets if b.id == tag.id]
    
    if not matching_baskets:
        return None
    matching_baskets.sort(key=lambda basket: basket.height, reverse=True)
    return matching_baskets[0]
    
    

def Drive_To_Basket():
    global CURRENT_FRUIT
    basket = detect_basket(CURRENT_FRUIT)
    if basket:
        basket_cx = basket.centerX
        target_cx = X_RESOLUTION/2
        print(type(basket))
        while (abs(basket_cx - target_cx) > 10 and basket.height < 30): #More Magic Numberds :)
            basket = detect_basket(CURRENT_FRUIT)
            if basket:
                basket_cx = basket.centerX
                error = basket_cx - target_cx
                left_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED - Fruit_PGain*error, DRIVE_MAX))
                right_motor.spin(REVERSE, clamp(DRIVE_MIN, DRIVE_SPEED + Fruit_PGain*error, DRIVE_MAX))
        left_motor.stop()
        right_motor.stop()
        print("Arrived in front of:" ,CURRENT_FRUIT, "basket")
        wait(0.02, SECONDS)
        
while True:
    #Detect Fruit
    if not HAVE_FRUIT:
        if (fruits := detect_fruits()):
            print("DETECTED A FRUIT")
            Approach_Fruit()
    if HAVE_FRUIT:
        Drive_To_Basket()
        
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
    #print(front_wall_distance)
    if front_wall_distance <= 400: # MM to detect end of field, Should Be 400
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


