from pimoroni import RGBLED, Button
from machine import Pin
from time import sleep
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2
display = PicoGraphics(DISPLAY_PICO_DISPLAY_2, rotate=0)

sprXtab = [140, 143, 147, 150, 154, 157, 161, 164, 167, 171, 174, 177, 181, 184, 187, 190, 194, 197, 200, 203, 206, 209, 212, 215, 218, 221, 223, 226, 229, 231, 234, 237, 239, 241, 244, 246, 248, 250, 252, 254, 256, 258, 260, 262, 263, 265, 267, 268, 269, 271, 272, 273, 274, 275, 276, 277, 277, 278, 278, 279, 279, 280, 280, 280, 280, 280, 280, 280, 279, 279, 278, 278, 277, 277, 276, 275, 274, 273, 272, 271, 269, 268, 267, 265, 263, 262, 260, 258, 256, 254, 252, 250, 248, 246, 244, 241, 239, 237, 234, 231, 229, 226, 223, 221, 218, 215, 212, 209, 206, 203, 200, 197, 194, 190, 187, 184, 181, 177, 174, 171, 167, 164, 161, 157, 154, 150, 147, 143, 140, 137, 133, 130, 126, 123, 119, 116, 113, 109, 106, 103, 99, 96, 93, 90, 86, 83, 80, 77, 74, 71, 68, 65, 62, 59, 57, 54, 51, 49, 46, 43, 41, 39, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18, 17, 15, 13, 12, 11, 9, 8, 7, 6, 5, 4, 3, 3, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 3, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 15, 17, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 39, 41, 43, 46, 49, 51, 54, 57, 59, 62, 65, 68, 71, 74, 77, 80, 83, 86, 90, 93, 96, 99, 103, 106, 109, 113, 116, 119, 123, 126, 130, 133, 136 ]
sprYtab = [100, 102, 105, 107, 110, 112, 115, 117, 120, 122, 124, 127, 129, 131, 134, 136, 138, 141, 143, 145, 147, 149, 151, 153, 156, 158, 160, 162, 163, 165, 167, 169, 171, 172, 174, 176, 177, 179, 180, 182, 183, 184, 186, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 196, 197, 198, 198, 199, 199, 199, 200, 200, 200, 200, 200, 200, 200, 200, 200, 199, 199, 199, 198, 198, 197, 196, 196, 195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 184, 183, 182, 180, 179, 177, 176, 174, 172, 171, 169, 167, 165, 163, 162, 160, 158, 156, 153, 151, 149, 147, 145, 143, 141, 138, 136, 134, 131, 129, 127, 124, 122, 120, 117, 115, 112, 110, 107, 105, 102, 100, 98, 95, 93, 90, 88, 85, 83, 80, 78, 76, 73, 71, 69, 66, 64, 62, 59, 57, 55, 53, 51, 49, 47, 44, 42, 40, 38, 37, 35, 33, 31, 29, 28, 26, 24, 23, 21, 20, 18, 17, 16, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 4, 3, 2, 2, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 2, 2, 3, 4, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 17, 18, 20, 21, 23, 24, 26, 28, 29, 31, 33, 35, 37, 38, 40, 42, 44, 47, 49, 51, 53, 55, 57, 59, 62, 64, 66, 69, 71, 73, 76, 78, 80, 83, 85, 88, 90, 93, 95, 98 ]

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

led = Pin(25, Pin.OUT)
swA = Pin(12, Pin.IN, Pin.PULL_UP)
swB = Pin(13, Pin.IN, Pin.PULL_UP)
swX = Pin(14, Pin.IN, Pin.PULL_UP)
swY = Pin(15, Pin.IN, Pin.PULL_UP)

from pngdec import PNG
png = PNG(display)

def setSpr(zx,zy):
        #Thank fsk I don't have to write a multiplexor !
    display.sprite(0,5,zx,zy)
    display.sprite(1,5,zx+8,zy)
    display.sprite(2,5,zx+16,zy)
    display.sprite(3,5,zx+24,zy)
    display.sprite(4,5,zx+32,zy)
    display.sprite(0,6,zx,zy+8)
    display.sprite(1,6,zx+8,zy+8)
    display.sprite(2,6,zx+16,zy+8)
    display.sprite(3,6,zx+24,zy+8)
    display.sprite(4,6,zx+32,zy+8)
    display.sprite(0,7,zx,zy+16)
    display.sprite(1,7,zx+8,zy+16)
    display.sprite(2,7,zx+16,zy+16)
    display.sprite(3,7,zx+24,zy+16)
    display.sprite(4,7,zx+32,zy+16)
    display.sprite(0,8,zx,zy+24)
    display.sprite(1,8,zx+8,zy+24)
    display.sprite(2,8,zx+16,zy+24)
    display.sprite(3,8,zx+24,zy+24)
    display.sprite(4,8,zx+32,zy+24)
    display.sprite(0,9,zx,zy+32)
    display.sprite(1,9,zx+8,zy+32)
    display.sprite(2,9,zx+16,zy+32)
    display.sprite(3,9,zx+24,zy+32)
    display.sprite(4,9,zx+32,zy+32)
    return

display.load_spritesheet("shinjitsu.rgb332")

for ss in range (1,7):
    st = str(ss) + ".png"
    print(st)
    png.open_file(st)
    png.decode(0, 0)
    display.update()
    sleep(.1)
png.open_file("main.png")
png.decode(0, 0)






sprX = 64
sprY = 0
locX = sprXtab[sprX]
locY = sprYtab[sprY]
buttonPressed = False
while not buttonPressed:
    if button_a.read():
        buttonPressed = True
        for name in dir():
            if not name.startswith('_'):
                del globals()[name]
        import spirit  
    if button_b.read():
        buttonPressed = True
        for name in dir():
            if not name.startswith('_'):
                del globals()[name]
        import world  
    if button_x.read():
        buttonPressed = True
        for name in dir():
            if not name.startswith('_'):
                del globals()[name]
        import wordsear 
    if button_y.read():
        buttonPressed = True
        for name in dir():
            if not name.startswith('_'):
                del globals()[name]
        import starfield   
    
    display.clear()
    sprX = (sprX + 254) & 255
    sprY = (sprY + 5) & 255
    print(sprX, sprY)
    print ("---")
    png.decode(0, 0)
    setSpr(sprXtab[sprX],sprYtab[sprY])

    display.update()
    
    #sleep(.1)

