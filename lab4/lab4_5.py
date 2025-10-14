from sense_hat import SenseHat
from random import randint
from time import sleep

sense = SenseHat()

def random_colour():
  random_red = randint(0, 255)
  random_green = randint(0, 255)
  random_blue = randint(0, 255)
  return (random_red, random_green, random_blue)
  
  
sense.show_letter("G", random_colour())
sleep(0.3)
sense.show_letter("A", random_colour())
sleep(0.3)
sense.show_letter("B", random_colour())
sleep(0.3)
sense.show_letter("I", random_colour())
sleep(0.3)
sense.clear()