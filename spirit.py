from machine import Pin
from random import choice, randrange
from time import sleep
import random
import binascii
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import jpegdec
from pimoroni import RGBLED, Button
import math
import machine
import time

yadj = 10
adcpin = 4
sensor = machine.ADC(adcpin)
  
def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

display = PicoGraphics(DISPLAY_PICO_DISPLAY_2, rotate=0)
WIDTH, HEIGHT = display.get_bounds()
SCALE = 1.5
SPACING = 1
WORD_WRAP = WIDTH -2

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

led = Pin(25, Pin.OUT)
swA = Pin(12, Pin.IN, Pin.PULL_UP)
swB = Pin(13, Pin.IN, Pin.PULL_UP)
swX = Pin(14, Pin.IN, Pin.PULL_UP)
swY = Pin(15, Pin.IN, Pin.PULL_UP)

def sw_handlerA(pin):
        sleep(5)
def sw_handlerB(pin):
        for name in dir():
            if not name.startswith('_'):
                del globals()[name]
        import main    
def sw_handlerX(pin):
        draw_jpg(display,"dlgbox.jpg")
        sleep(5)
def sw_handlerY(pin):
        draw_jpg(display,"tccgbox.jpg")
        sleep(5)

swA.irq(trigger = machine.Pin.IRQ_FALLING, handler = sw_handlerA)
swB.irq(trigger = machine.Pin.IRQ_FALLING, handler = sw_handlerB)
swX.irq(trigger = machine.Pin.IRQ_FALLING, handler = sw_handlerX)
swY.irq(trigger = machine.Pin.IRQ_FALLING, handler = sw_handlerY)

display.set_backlight(0.5)
led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

white = {'red': 255, 'green': 255, 'blue': 255}
red4 = {'red': 255-64, 'green': 96, 'blue': 128}
red3 = {'red': (255-64), 'green': 64, 'blue': 128}
red2 = {'red': (255-64), 'green': 32, 'blue': 128}
red = {'red': (255-64), 'green': 255, 'blue': 128}
black = {'red': 0, 'green': 0, 'blue': 0}

def draw_jpg(display, filename):
    j = jpegdec.JPEG(display)
    j.open_file(filename)
    WIDTH, HEIGHT = display.get_bounds()
    #display.set_clip(0, 0, WIDTH, HEIGHT)
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)
    #display.remove_clip()
    display.update()

GHOST_WORDS = "my999.txt"
BACKGROUND = "shinjitsu.jpg"
BACKGROUND2 = "ghostbox3.jpg"
MIN_WAIT = 5
MAX_WAIT = 10
w1 = ""
w2 = ""
w3 = ""
w4 = ""

def load_ghost_words():
    with open(GHOST_WORDS, "r") as f:
        return f.read().splitlines()
draw_jpg(display,BACKGROUND2)


# load the ghost words
words = load_ghost_words()

white_pen = display.create_pen(white['red'],white['green'],white['blue'])
red_pen = display.create_pen(red['red'],red['green'],red['blue'])
red2_pen = display.create_pen(red2['red'],red2['green'],red2['blue'])
red3_pen = display.create_pen(red3['red'],red3['green'],red3['blue'])
red4_pen = display.create_pen(red4['red'],red4['green'],red4['blue'])
black_pen = display.create_pen(black['red'],black['green'],black['blue'])

display.set_font('serif')
display.set_thickness(3)

buttonPressed = False
while not buttonPressed:
    waitvar = int(ReadTemperature()) & 7
    wait = ((randrange(MIN_WAIT, MAX_WAIT) ^ waitvar) & 7) + 5
    display.set_pen(black_pen)
    display.clear()
    draw_jpg(display,BACKGROUND)
    display.update()
    # pick a random word
    word = choice(words)
    waitvar = int(ReadTemperature()) ^ random.randrange(1, 999) * 3 ^ 31337 * 12939
    #Seed with a Pseudo/Entropy random value hash
    random.seed(waitvar)
    out = (random.randrange(1, 999))
    word = words[out]
    
    #display.set_pen(white_pen)
    w1 = w2
    w2 = w3
    w3 = w4
    w4 = word
    
    display.set_pen(red_pen)
    length = display.measure_text(w4,SCALE,SPACING)
    mid_point = WIDTH //2
    x = mid_point - ( length // 2)
    y = 200 + yadj
    display.text(w4, x,y,WORD_WRAP,SCALE)
    
    display.set_pen(red2_pen)
    length = display.measure_text(w3,SCALE,SPACING)
    mid_point = WIDTH //2
    x = mid_point - ( length // 2)
    y = 150 + yadj
    display.text(w3, x,y,WORD_WRAP,SCALE)
    
    display.set_pen(red3_pen)
    length = display.measure_text(w2,SCALE,SPACING)
    mid_point = WIDTH //2
    x = mid_point - ( length // 2)
    y = 100 + yadj
    display.text(w2, x,y,WORD_WRAP,SCALE)
    
    display.set_pen(red4_pen)
    length = display.measure_text(w1,SCALE,SPACING)
    mid_point = WIDTH //2
    x = mid_point - ( length // 2)
    y = 50 + yadj
    display.text(w1, x,y,WORD_WRAP,SCALE)
    display.update()
    
    sleep(wait)




