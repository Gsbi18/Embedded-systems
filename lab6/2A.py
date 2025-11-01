from sense_hat import SenseHat
import time

sense = SenseHat()
states = 0
w = (255,255,255)
r = (255,0,0)
g = (0,255,0)
y = (255,255,0)
n = (0,0,0)
red = [
n, n, n, r, r, n, n, n,
n, n, n, r, r, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n
]
red_yellow = [
n, n, n, r, r, n, n, n,
n, n, n, r, r, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, y, y, n, n, n,
n, n, n, y, y, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n
]
yellow = [
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, y, y, n, n, n,
n, n, n, y, y, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n
]
green = [
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, n, n, n, n, n,
n, n, n, g, g, n, n, n,
n, n, n, g, g, n, n, n
]
  
def state(color,duration):
    if color == 'red':
        sense.set_pixels(red)
        time.sleep(duration)
        sense.clear()
    elif color == 'red_yellow':
        sense.set_pixels(red_yellow)
        time.sleep(duration)
        sense.clear()
    elif color == 'yellow':
        sense.set_pixels(yellow)
        time.sleep(duration)
        sense.clear()
    elif color == 'green':
        sense.set_pixels(green)
        time.sleep(duration)
        sense.clear()
    elif color=='none':
        sense.set_pixels(yellow)
        time.sleep(0.5)
        sense.clear()
        time.sleep(0.5)
        
def set_state():
    global states
    # state variable has been defined outside
    if states < 3:
        states += 1
    elif states == 3:
        states = 0   
    else:
        pass
    
def button_event(event):
    global states
    if event.action == 'released':
        if states != 4:
            states = 4
        else:
            states = 3
sense.stick.direction_middle = button_event

def main():
    global states
    while True:
        if states == 0:
            state('red',3)
        elif states == 1:
            state('red_yellow',1)
        elif states == 2:
            state('green',2)
        elif states == 3:
           state('yellow',1)
        else:
            state('none')    
        set_state()
        
if __name__ == "__main__":
    main()