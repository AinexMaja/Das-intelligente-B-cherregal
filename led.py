import time
import board
import neopixel

#Connection from Data In to the LED-Strip on Pin D18
pixel_pin = board.D14

# The number of NeoPixels
num_pixels = 796

# The order of the pixel colors - RGB or GRB (Some NeoPixels have red and green reverse)
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def flashLED(positions, widths):
    if type(positions) != type([]):
        positions = [positions]
        widths = [widths]
        print(positions, widths)
    for position, width in zip(positions, widths):
        index1 = (position[0]+20.0)/0.625
        index1 = int(index1)
        index2 = (position[0]+20.0+width[0])/0.625
        index2 = int(index2)
        for i in range(index1, index2):
            pixels[i] = (255,0,255)
    pixels.show()
