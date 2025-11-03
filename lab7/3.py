from sense_hat import SenseHat
import random
from time import sleep

sense = SenseHat()
speed = 0.4  
score = 0

w = (0, 0, 0)    
r = (255, 0, 0)   
b = (0, 0, 255)   

basket = [7, 4]

game_space = [w] * 64
game_space[8*7 + (basket[1]-1)] = b
game_space[8*7 +  basket[1]   ] = b

def update_space(x, y, colour):
    if 0 <= x <= 7 and 0 <= y <= 7:
        p = 8 * x + y
        game_space[p] = colour
        sense.set_pixels(game_space)

def left(event):
    if event.action == 'pressed':
        if (basket[1] - 1) == 0:
            return
        update_space(basket[0], basket[1], w)
        basket[1] -= 1
        update_space(basket[0], basket[1] - 1, b)

def right(event):
    if event.action == 'pressed':
        if (basket[1] + 1) == 8:
            return
        update_space(basket[0], basket[1] - 1, w)
        basket[1] += 1
        update_space(basket[0], basket[1], b)

sense.stick.direction_left = left
sense.stick.direction_right = right

sense.clear()
sense.set_pixels(game_space)

x = 0
y = random.randint(0, 7)
d = random.choice([-1, 1])  
updown = 1                  
update_space(x, y, r)

game_alive = True

while game_alive:
    sleep(speed)
    update_space(x, y, w)

    if y == 7 and d == 1:
        d = -1
    elif y == 0 and d == -1:
        d = 1

    if x == 0 and updown == -1:
        updown = 1
    if x == 7:
        if y == basket[1] or y == (basket[1] - 1):
            updown = -1
            score += 1
        else:
            game_alive = False
    x += updown
    y += d
    if game_alive:
        update_space(x, y, r)
sense.clear()
sense.show_message('Game over!', scroll_speed=0.05, back_colour=w)
sense.show_message('Score: ' + str(score), scroll_speed=0.05, back_colour=w)
