import time
import board
import neopixel
import threading
import numpy as np

COLORS = [(255, 0, 0), (255, 0, 50), (255, 0, 255), (128, 0, 255), (0, 0, 255)]

#Connection from Data In to the LED-Strip on Pin D18
pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 300

# The order of the pixel colors - RGB or GRB (Some NeoPixels have red and green reverse)
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)

def flashLED(positions, widths):
    if type(positions) != type(np.array([])):
        positions = [positions]
        widths = [widths]
        print(positions, widths)
    color_idx = 0
    for position, width in zip(positions, widths):
        print(position, width)
        index1 = (position[0]+26.5)/0.625
        index1 = int(index1)
        index2 = (position[0]+26.5+width[0])/0.625
        index2 = int(index2)
        for i in range(index1, index2):
            pixels[i] = COLORS[color_idx]
        color_idx += 1
        if color_idx == len(COLORS):
            color_idx = 0
    pixels.show()


def clearLEDs():
# Alle LEDs ausschalten
    for i in range(len(pixels)):
        pixels[i] = (0, 0, 0)
        pixels.show()


# Asynchrone Version der Funktionen
def flashLED_async(positions, widths):
    thread = threading.Thread(target=flashLED, args=(positions, widths))
    thread.start()

def clearLEDs_async():
    thread = threading.Thread(target=clearLEDs)
    thread.start()        
