from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
r = (255, 0, 0)     
b = (0, 0, 0)        

arrow_up = [
    b,b,b,r,b,b,b,b,
    b,b,r,r,r,b,b,b,
    b,r,b,r,b,r,b,b,
    r,b,b,r,b,b,r,b,
    b,b,b,r,b,b,b,b,
    b,b,b,r,b,b,b,b,
    b,b,b,r,b,b,b,b,
    b,b,b,b,b,b,b,b]

arrow_down = [
    b,b,b,r,b,b,b,b,
    b,b,b,r,b,b,b,b,
    b,b,b,r,b,b,b,b,
    r,b,b,r,b,b,r,b,
    b,r,b,r,b,r,b,b,
    b,b,r,r,r,b,b,b,
    b,b,b,r,b,b,b,b,
    b,b,b,b,b,b,b,b]

arrow_left = [
    b,b,b,r,b,b,b,b,
    b,b,r,b,b,b,b,b,
    b,r,b,b,b,b,b,b,
    r,r,r,r,r,r,r,b,
    b,r,b,b,b,b,b,b,
    b,b,r,b,b,b,b,b,
    b,b,b,r,b,b,b,b,
    b,b,b,b,b,b,b,b]

arrow_right = [
    b,b,b,b,r,b,b,b,
    b,b,b,b,b,r,b,b,
    b,b,b,b,b,b,r,b,
    b,r,r,r,r,r,r,r,
    b,b,b,b,b,b,r,b,
    b,b,b,b,b,r,b,b,
    b,b,b,b,r,b,b,b,
    b,b,b,b,b,b,b,b]

while True:
  for event in sense.stick.get_events():
    if event.action == "pressed":
# Check which direction
      if event.direction == "up":
        sense.set_pixels(arrow_up) # Up arrow
      elif event.direction == "down":
        sense.set_pixels(arrow_down) # Down arrow
      elif event.direction == "left":
        sense.set_pixels(arrow_left) # Left arrow
      elif event.direction == "right":
        sense.set_pixels(arrow_right) # Right arrow
      elif event.direction == "middle":
        sense.show_letter("M") # Enter key
      sleep(0.5)
      sense.clear()