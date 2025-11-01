from sense_hat import SenseHat
import time
import random

sense = SenseHat()

space_size = 8
delay_s = 0.5 
n = (0, 0, 0)  
b = (0, 0, 255) 

space = [n for _ in range(space_size * space_size)]

def idx(x, y):
    return y * space_size + x

def shift_down():
    global space
    for y in range(space_size - 1, 0, -1):
        for x in range(space_size):
            space[idx(x, y)] = space[idx(x, y - 1)]
    for x in range(space_size):
        space[idx(x, 0)] = n

def spawn_drop_top():
    x = random.randint(0, space_size - 1)
    space[idx(x, 0)] = b

def main():
    try:
        sense.set_pixels(space)
        while True:
            spawn_drop_top()
            sense.set_pixels(space)
            time.sleep(delay_s)
            shift_down()
            sense.set_pixels(space)
    except KeyboardInterrupt:
        pass
    finally:
        sense.clear()

if __name__ == "__main__":
    main()
