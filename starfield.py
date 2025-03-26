# Travel through a Windows 3.1-esque starfield, with stars growing as they get 'closer'.
# If you have a Display Pack 2.0" or 2.8" use DISPLAY_PICO_DISPLAY_2 instead of DISPLAY_PICO_DISPLAY

from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import random
from pimoroni import RGBLED, Button
import math
import machine
import time

# Constants to play with
NUMBER_OF_STARS = 256*4
TRAVEL_SPEEDX = 2.3
TRAVEL_SPEEDY = 3.2
STAR_GROWTH = 0.3
button_b = Button(13)
led = RGBLED(6, 7, 8)
led.set_rgb(0,32,32)

# Set up our display
graphics = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2)

WIDTH, HEIGHT = graphics.get_bounds()

#BLACK = graphics.create_pen(0, 0, 0)
BLACK = graphics.create_pen(64, 0, 64)
#WHITE = graphics.create_pen(255, 255, 255)
WHITE = graphics.create_pen(255, 255, 255)

stars = []
graphics.set_backlight(.8)
adcpin = 4
sensor = machine.ADC(adcpin)

def new_star():
    star = [random.randint(0, WIDTH) - WIDTH // 2, random.randint(0, HEIGHT) - HEIGHT // 2, 0.5]
    return star

def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

for i in range(0, NUMBER_OF_STARS):
    stars.append(new_star())

buttonPressed = False

while not buttonPressed:
    graphics.set_pen(BLACK)
    graphics.clear()
    graphics.set_pen(WHITE)
    for i in range(0, NUMBER_OF_STARS):
        s = stars[i]
        s[0] = s[0] * TRAVEL_SPEEDX
        s[1] = s[1] * TRAVEL_SPEEDY
        if s[0] <= - WIDTH // 2 or s[0] >= WIDTH // 2 or s[1] <= - HEIGHT // 2 or s[1] >= HEIGHT // 2 or s[2] >= 5:
            s = new_star()
        s[2] += STAR_GROWTH
        stars[i] = s
        graphics.circle(int(s[0]) + WIDTH // 2, int(s[1]) + HEIGHT // 2, int(s[2]))
    TRAVEL_SPEEDX = waitvar = (int(ReadTemperature()) & 7) +1
    TRAVEL_SPEEDY = waitvar = (int(ReadTemperature()) & 15 ^ 2) +1
    graphics.update()
    if button_b.read():
            buttonPressed = True

for name in dir():
    if not name.startswith('_'):
        del globals()[name]

import main
