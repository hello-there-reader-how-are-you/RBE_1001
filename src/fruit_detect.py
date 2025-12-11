def fruit_detect(fruit):
    global current_state, missed_detections, CURRENT_FRUIT

    cx = fruit.centerX
    cy = fruit.centerY

    if fruit.id == 1:
        CURRENT_FRUIT = "green"
    elif fruit.id == 2:
        CURRENT_FRUIT = "purple"
    elif fruit.id == 3:
        CURRENT_FRUIT = "orange"
    else:
        CURRENT_FRUIT = "unknown"

def Drive_To_Basket():
    global CURRENT_FRUIT
    basket = detect_basket(CURRENT_FRUIT)
    if basket:
        basket_cx = basket.centerX
        target_cx = X_RESOLUTION/2
        while abs(basket_cx - target_cx) > 10:
            basket = detect_basket(CURRENT_FRUIT)
            if basket:
                basket_cx = basket.centerX
                error = basket_cx - target_cx
                left_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED - Fruit_PGain*error, DRIVE_MAX))
                right_motor.spin(FORWARD, clamp(DRIVE_MIN, DRIVE_SPEED + Fruit_PGain*error, DRIVE_MAX))
        left_motor.stop()
        right_motor.stop()
        print("Arrived in front of {CURRENT_FRUIT} basket")
      
