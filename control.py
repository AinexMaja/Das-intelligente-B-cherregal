import time
import board
import neopixel

#Connection from Data In to the LED-Strip on Pin D18
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 796

# The order of the pixel colors - RGB or GRB (Some NeoPixels have red and green reverse)
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def flashLED(pos):
    pixels[pos] = (255,255,255)
    pixels.show()

def flashLED2(length):
    pos = length/0.625
    pos = int(pos)
    pixels[pos] = (255,0,0)
    pixels.show()

def test():
    pixels[0] = (255,255,255)
    pixels[1] = (255,0,0)
    pixels[2] = (0,255,0)
    pixels[3] = (255,255,255)
    pixels[4] = (255,0,0)
    pixels.show()


while True:
    #flashLED(0)
    flashLED2(200)
    #test()