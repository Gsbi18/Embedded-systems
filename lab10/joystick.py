from sense_hat import SenseHat, ACTION_PRESSED
import random
import time

sense = SenseHat()
sense.clear()

COLOR = (255, 0, 0)

x = random.randint(0, 7)
y = random.randint(0, 7)

def draw_pixel(x, y):
    sense.clear()
    sense.set_pixel(x, y, COLOR)

draw_pixel(x, y)

print("A joystickon a középső gombbal állíthatod le.")
flag= True
while flag:
    events = sense.stick.get_events()
    if not events:
        time.sleep(0.05)
        continue

    for event in events:
        if event.action != ACTION_PRESSED:
            continue

        direction = event.direction

        if direction == "up":
            if y > 0:
                y -= 1
        elif direction == "down":
            if y < 7:
                y += 1
        elif direction == "left":
            if x > 0:
                x -= 1
        elif direction == "right":
            if x < 7:
                x += 1
        elif direction == "middle":
            flag = False
            sense.clear()
            break
        draw_pixel(x, y)
