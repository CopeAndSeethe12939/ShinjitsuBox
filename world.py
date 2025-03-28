import time
import math
import picographics
from pimoroni import Button
import jpegdec
import machine


sensor = machine.ADC(4) #Temp Sensor Pin 4

sprXtab = [156, 160, 164, 167, 171, 175, 179, 183, 186, 190, 194, 198, 201, 205, 209, 212, 216, 219, 223, 226, 230, 233, 236, 239, 243, 246, 249, 252, 255, 258, 261, 264, 266, 269, 272, 274, 277, 279, 281, 284, 286, 288, 290, 292, 294, 295, 297, 299, 300, 302, 303, 304, 305, 306, 307, 308, 309, 310, 310, 311, 311, 312, 312, 312, 312, 312, 312, 312, 311, 311, 310, 310, 309, 308, 307, 306, 305, 304, 303, 302, 300, 299, 297, 295, 294, 292, 290, 288, 286, 284, 281, 279, 277, 274, 272, 269, 266, 264, 261, 258, 255, 252, 249, 246, 243, 239, 236, 233, 230, 226, 223, 219, 216, 212, 209, 205, 201, 198, 194, 190, 186, 183, 179, 175, 171, 167, 164, 160, 156, 152, 148, 145, 141, 137, 133, 129, 126, 122, 118, 114, 111, 107, 103, 100, 96, 93, 89, 86, 82, 79, 76, 73, 69, 66, 63, 60, 57, 54, 51, 48, 46, 43, 40, 38, 35, 33, 31, 28, 26, 24, 22, 20, 18, 17, 15, 13, 12, 10, 9, 8, 7, 6, 5, 4, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 15, 17, 18, 20, 22, 24, 26, 28, 31, 33, 35, 38, 40, 43, 46, 48, 51, 54, 57, 60, 63, 66, 69, 73, 76, 79, 82, 86, 89, 93, 96, 100, 103, 107, 111, 114, 118, 122, 126, 129, 133, 137, 141, 145, 148, 152 ]
sprYtab = [116, 119, 122, 125, 127, 130, 133, 136, 139, 141, 144, 147, 150, 152, 155, 158, 160, 163, 166, 168, 171, 173, 176, 178, 180, 183, 185, 187, 190, 192, 194, 196, 198, 200, 202, 204, 206, 207, 209, 211, 212, 214, 215, 217, 218, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 229, 230, 230, 231, 231, 231, 232, 232, 232, 232, 232, 232, 232, 231, 231, 231, 230, 230, 229, 229, 228, 227, 226, 225, 224, 223, 222, 221, 220, 218, 217, 215, 214, 212, 211, 209, 207, 206, 204, 202, 200, 198, 196, 194, 192, 190, 187, 185, 183, 180, 178, 176, 173, 171, 168, 166, 163, 160, 158, 155, 152, 150, 147, 144, 141, 139, 136, 133, 130, 127, 125, 122, 119, 116, 113, 110, 107, 105, 102, 99, 96, 93, 91, 88, 85, 82, 80, 77, 74, 72, 69, 66, 64, 61, 59, 56, 54, 52, 49, 47, 45, 42, 40, 38, 36, 34, 32, 30, 28, 26, 25, 23, 21, 20, 18, 17, 15, 14, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 17, 18, 20, 21, 23, 25, 26, 28, 30, 32, 34, 36, 38, 40, 42, 45, 47, 49, 52, 54, 56, 59, 61, 64, 66, 69, 72, 74, 77, 80, 82, 85, 88, 91, 93, 96, 99, 102, 105, 107, 110, 113]

display = picographics.PicoGraphics(picographics.DISPLAY_PICO_DISPLAY_2, pen_type=picographics.PEN_RGB332, rotate=0)
WHITE = display.create_pen(255,255,255)
BLACK = display.create_pen(0,0,0)
button_a = Button(12)
button_b = Button(13)

def clear():
    display.set_pen(BLACK)
    display.clear()
    display.update()
    return

def initDisplay():
    clear()
    display.set_backlight(0.5)
    return
    
def showMap():
    clear()
    display.load_spritesheet("spriteSheet.rgb332")
    buttonPressed = False
    while not buttonPressed:
        cnt = 0
        cntx = 64
        while (not buttonPressed):
            display.sprite(0,0,sprXtab[cnt],sprYtab[cntx])

            display.update()
            
            cnt = (cnt + (int(ReadTemperature()) & 3)) & 255
            cntx = (cntx + (int(ReadTemperature()) & 3) + 1) & 255
            if button_b.read():
                buttonPressed = True
        clear()
        return
    
def ReadTemperature():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)

#INIT here
initDisplay()
showMap()
for name in dir():
    if not name.startswith('_'):
        del globals()[name]
del name, __name__
import main

