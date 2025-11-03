from sense_hat import SenseHat
from time import sleep
import random

sense = SenseHat()
sense.clear()

W = (0, 0, 0)     
H = (0, 255, 0)      
S = (0, 150, 0)     
F = (255, 0, 0)      

BASE_SPEED = 0.30    
MIN_SPEED  = 0.08   
SPEED_GAIN = 0.96    

direction = (1, 0)  
speed = BASE_SPEED
score = 0

snake = [(3, 4), (2, 4), (1, 4)] 
food = None

def draw():
    buf = [W] * 64
    if food:
        fx, fy = food
        buf[8 * fy + fx] = F
    for (x, y) in snake[1:]:
        buf[8 * y + x] = S
        
    hx, hy = snake[0]
    buf[8 * hy + hx] = H
    sense.set_pixels(buf)

def random_empty_cell():
    free = {(x, y) for x in range(8) for y in range(8)} - set(snake)
    return random.choice(list(free)) if free else None

def place_food():
    global food
    food = random_empty_cell()

def opposite(a, b):
    return a[0] == -b[0] and a[1] == -b[1]

def go_up(event):
    global direction
    if event.action == "pressed":
        nd = (0, -1)
        if not opposite(direction, nd):
            direction = nd

def go_down(event):
    global direction
    if event.action == "pressed":
        nd = (0, 1)
        if not opposite(direction, nd):
            direction = nd

def go_left(event):
    global direction
    if event.action == "pressed":
        nd = (-1, 0)
        if not opposite(direction, nd):
            direction = nd

def go_right(event):
    global direction
    if event.action == "pressed":
        nd = (1, 0)
        if not opposite(direction, nd):
            direction = nd

sense.stick.direction_up = go_up
sense.stick.direction_down = go_down
sense.stick.direction_left = go_left
sense.stick.direction_right = go_right

place_food()
draw()

alive = True
while alive:
    sleep(speed)

    dx, dy = direction
    hx, hy = snake[0]
    nx, ny = hx + dx, hy + dy

    if nx < 0 or nx > 7 or ny < 0 or ny > 7 or (nx, ny) in snake:
        alive = False
        break

    snake.insert(0, (nx, ny))

    if food and (nx, ny) == food:
        score += 1
        speed = max(MIN_SPEED, speed * SPEED_GAIN)
        place_food()
    else:
        snake.pop()

    draw()
sense.clear()
sense.show_message("Game Over", scroll_speed=0.05, back_colour=W)
sense.show_message("Score: " + str(score), scroll_speed=0.05, back_colour=W)
sense.clear()
