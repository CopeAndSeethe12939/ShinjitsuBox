from machine import Pin
from random import choice, randrange
import random
import binascii
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
import jpegdec
from time import sleep
from pimoroni import RGBLED, Button
import gc
import math
import machine

#Set start of planchette
px = 3
py = 3
pz = 0

#Sine table of all screen locations (minus 8 pixels for sprite)
sprXtab = [140, 143, 147, 150, 154, 157, 161, 164, 167, 171, 174, 177, 181, 184, 187, 190, 194, 197, 200, 203, 206, 209, 212, 215, 218, 221, 223, 226, 229, 231, 234, 237, 239, 241, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 263, 265, 267, 268, 269, 271, 272, 273, 274, 275, 276, 277, 277, 278, 278, 279, 279, 280, 280, 280, 280, 280, 280, 280, 279, 279, 278, 278, 277, 277, 276, 275, 274, 273, 272, 271, 269, 268, 267, 265, 263, 262, 260, 258, 256, 254, 252, 250, 248, 246, 244, 241, 239, 237, 234, 231, 229, 226, 223, 221, 218, 215, 212, 209, 206, 203, 200, 197, 194, 190, 187, 184, 181, 177, 174, 171, 167, 164, 161, 157, 154, 150, 147, 143, 140, 137, 133, 130, 126, 123, 119, 116, 113, 109, 106, 103, 99, 96, 93, 90, 86, 83, 80, 77, 74, 71, 68, 65, 62, 59, 57, 54, 51, 49, 46, 43, 41, 39, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18, 17, 15, 13, 12, 11, 9, 8, 7, 6, 5, 4, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 17, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 39, 41, 43, 46, 49, 51, 54, 57, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 90, 93, 96, 99, 103, 106, 109, 113, 116, 119, 123, 126, 130, 133, 136 ]
sprYtab = [100, 102, 105, 107, 110, 112, 115, 117, 120, 122, 124, 127, 129, 131, 134, 136, 138, 141, 143, 145, 147, 149, 151, 153, 156, 158, 160, 162, 163, 165, 167, 169, 171, 172, 174, 176, 177, 179, 180, 182, 183, 184, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 196, 197, 198, 198, 199, 199, 199, 200, 200, 200, 200, 200, 200, 200, 200, 200, 199, 199, 199, 198, 198, 197, 196, 196, 195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 184, 183, 182, 180, 179, 177, 176, 174, 172, 171, 169, 167, 165, 163, 162, 160, 158, 156, 153, 151, 149, 147, 145, 143, 141, 138, 136, 134, 131, 129, 127, 124, 122, 120, 117, 115, 112, 110, 107, 105, 102, 100, 98, 95, 93, 90, 88, 85, 83, 80, 78, 76, 73, 71, 69, 66, 64, 62, 59, 57, 55, 53, 51, 49, 47, 44, 42, 40, 38, 37, 35, 33, 31, 29, 28, 26, 24, 23, 21, 20, 18, 17, 16, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 4, 3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 20, 21, 23, 24, 26, 28, 29, 31, 33, 35, 37, 38, 40, 42, 44, 47, 49, 51, 53, 55, 57, 59, 62, 64, 66, 69, 71, 73, 76, 78, 80, 83, 85, 88, 90, 93, 95, 98]

#Random Entropy table from random.org
sprRnd = [5,2,5,6,1,7,7,1,2,7,5,3,3,2,3,3,7,7,3,7,3,4,2,6,4,4,6,3,2,1,1,7,
3,1,5,2,0,0,7,2,4,4,6,0,0,4,7,0,3,7,6,4,7,3,5,4,0,4,5,6,5,6,0,0,
5,7,4,0,1,5,0,6,1,7,1,0,1,5,6,0,7,6,6,7,3,6,4,5,0,7,1,0,3,2,7,3,
7,0,6,3,2,2,6,0,0,5,6,3,3,4,5,6,4,4,6,3,6,6,4,6,6,0,4,0,3,1,0,1,
7,1,3,4,7,6,2,1,3,2,7,5,5,2,4,4,2,7,2,4,3,1,2,4,6,0,0,6,3,6,1,6,
3,7,0,4,6,7,2,3,7,7,3,1,1,4,3,3,4,5,1,4,4,7,0,0,3,0,2,2,5,2,6,2,
6,3,0,1,2,4,0,6,4,4,6,4,1,3,4,5,4,5,4,7,3,1,7,5,2,0,4,6,2,0,5,6,
5,6,0,3,7,0,7,0,4,3,0,2,5,6,6,3,1,3,3,2,6,6,7,1,5,6,2,5,7,7,1,5]

def draw_jpg():
    return

def setSpr(zx,zy):
        #Thank fsk I don't have to write a multiplexor !
    display.sprite(0,0,zx,zy)
    display.sprite(1,0,zx+8,zy)
    display.sprite(2,0,zx+16,zy)
    display.sprite(3,0,zx+24,zy)
    display.sprite(4,0,zx+32,zy)
    display.sprite(0,1,zx,zy+8)
    display.sprite(1,1,zx+8,zy+8)
    display.sprite(2,1,zx+16,zy+8)
    display.sprite(3,1,zx+24,zy+8)
    display.sprite(4,1,zx+32,zy+8)
    display.sprite(0,2,zx,zy+16)
    display.sprite(1,2,zx+8,zy+16)
    display.sprite(2,2,zx+16,zy+16)
    display.sprite(3,2,zx+24,zy+16)
    display.sprite(4,2,zx+32,zy+16)
    display.sprite(0,3,zx,zy+24)
    display.sprite(1,3,zx+8,zy+24)
    display.sprite(2,3,zx+16,zy+24)
    display.sprite(3,3,zx+24,zy+24)
    display.sprite(4,3,zx+32,zy+24)
    display.sprite(0,4,zx,zy+32)
    display.sprite(1,4,zx+8,zy+32)
    display.sprite(2,4,zx+16,zy+32)
    display.sprite(3,4,zx+24,zy+32)
    display.sprite(4,4,zx+32,zy+32)
    return

def upSpr():
        #Thank fsk I don't have to write a multiplexor !
    display.sprite(0,0,px,py)
    display.sprite(1,0,px+8,py)
    display.sprite(2,0,px+16,py)
    display.sprite(3,0,px+24,py)
    display.sprite(4,0,px+32,py)
    display.sprite(0,1,px,py+8)
    display.sprite(1,1,px+8,py+8)
    display.sprite(2,1,px+16,py+8)
    display.sprite(3,1,px+24,py+8)
    display.sprite(4,1,px+32,py+8)
    display.sprite(0,2,px,py+16)
    display.sprite(1,2,px+8,py+16)
    display.sprite(2,2,px+16,py+16)
    display.sprite(3,2,px+24,py+16)
    display.sprite(4,2,px+32,py+16)
    display.sprite(0,3,px,py+24)
    display.sprite(1,3,px+8,py+24)
    display.sprite(2,3,px+16,py+24)
    display.sprite(3,3,px+24,py+24)
    display.sprite(4,3,px+32,py+24)
    display.sprite(0,4,px,py+32)
    display.sprite(1,4,px+8,py+32)
    display.sprite(2,4,px+16,py+32)
    display.sprite(3,4,px+24,py+32)
    display.sprite(4,4,px+32,py+32)
    return

def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

#gc.collect()

display = PicoGraphics(DISPLAY_PICO_DISPLAY_2, rotate=0)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

led = RGBLED(6, 7, 8)
led.set_rgb(0,0,0)
adcpin = 4
sensor = machine.ADC(adcpin)

WIDTH, HEIGHT = display.get_bounds()
SCALE = .9
SPACING = 1
WORD_WRAP = WIDTH -4
display.set_font('sans')
display.set_thickness(3)
display.set_backlight(1)

w1 = "1 2 3 4 5 6 7 8 9 0"
w2 = "q w e r t y u i o p"
w3 = " a s d f g h j k l "
w4 = "   z x c v b n m "

red = {'red': (255-80), 'green': 0, 'blue': 128}
red2 = {'red': (255-96), 'green': 0, 'blue': 128}
red3 = {'red': (255-112), 'green': 0, 'blue': 128}
red4 = {'red': (255-128), 'green': 0, 'blue': 128}
red_pen = display.create_pen(red['red'],red['green'],red['blue'])
red2_pen = display.create_pen(red2['red'],red2['green'],red2['blue'])
red3_pen = display.create_pen(red3['red'],red3['green'],red3['blue'])
red4_pen = display.create_pen(red4['red'],red4['green'],red4['blue'])

display.load_spritesheet("shinjitsu.rgb332")

def ShowTable():
    display.set_pen(red_pen)
    length = display.measure_text(w4,SCALE,SPACING)
    mid_point = WIDTH //2
    x = mid_point - ( length // 2)
    y = 200
    display.text(w4, x,y,WORD_WRAP,SCALE)
    
    display.set_pen(red2_pen)
    length = display.measure_text(w3,SCALE,SPACING)
    mid_point = WIDTH //2
    x = mid_point - ( length // 2)
    y = 150
    display.text(w3, x,y,WORD_WRAP,SCALE)
    
    display.set_pen(red3_pen)
    length = display.measure_text(w2,SCALE,SPACING)
    mid_point = WIDTH //2
    x = mid_point - ( length // 2)
    y = 100
    display.text(w2, x,y,WORD_WRAP,SCALE)
    
    display.set_pen(red4_pen)
    length = display.measure_text(w1,SCALE,SPACING)
    mid_point = WIDTH //2
    x = mid_point - ( length // 2)
    y = 50
    display.text(w1, x,y,WORD_WRAP,SCALE)
    
    return

ax = 0
ay = 0

draw_jpg()
buttonPressed = False

while not buttonPressed:

    # Use 7 bits of Internal Temp
    waitvar = int(ReadTemperature()) & 127
    wait = ((randrange(3, 5) ^ waitvar) & 7) + 3
  
    while (ax != px) and (ay != py):
        wait = ((randrange(3, 5) ^ waitvar) & 7) + 3
        if ax < px:
            ax = ax + sprRnd[wait]
            if ax > px:
                ax = px
        if ax > px:
            ax = ax - sprRnd[wait]
            if ax < px:
                ax = px
        if ay < py:
            ay = ay + sprRnd[wait]
            if ay > py:
                ay = py
        if ay > py:
            ay = ay - sprRnd[wait]
            if ay < py:
                ay = py
        display.clear()
        print (ay,ax)
        ShowTable()
        setSpr(ax,ay)
        display.update()
        
        if button_b.read():
                buttonPressed = True
        
    display.clear()
    ShowTable()
    upSpr()
    
    for Wooper in range (3):
    #PseudoRND with IRL entropic value for X/Y values
        pa = random.randint(0, 255) ^ 127
        pz = random.randint(0, 255) ^ 255
        px = px + (((sprXtab[sprRnd[pa]] + int((ReadTemperature())) ^ 11939) ) ) & 255
        py = py + (((sprYtab[sprRnd[pz]] + int((ReadTemperature()))) * 19937) ) & 255
    led.set_rgb(64,0,64)
    #print ("dump: ",ax,ay)
    sleep(wait)
    
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
import main
