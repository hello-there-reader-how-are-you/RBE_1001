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
