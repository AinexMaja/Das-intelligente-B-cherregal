import time
import board
import neopixel

# Pin definitions for each NeoPixel strip
pixel_pin_1 = board.D18
pixel_pin_2 = board.D12
pixel_pin_3 = board.D21

# Number of NeoPixels on each strip (assuming the same number for simplicity)
num_pixels = 628

# The order of the pixel colors - RGB or GRB. Adjust if necessary.
ORDER = neopixel.GRB

# Create NeoPixel objects for each strip
pixels_1 = neopixel.NeoPixel(pixel_pin_1, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
pixels_2 = neopixel.NeoPixel(pixel_pin_2, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)
pixels_3 = neopixel.NeoPixel(pixel_pin_3, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER)

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    return (r, g, b) if ORDER in (neopixel.RGB, neopixel.GRB) else (r, g, b, 0)

def rainbow_cycle(wait):
    for j in range(255):
        for i in range(num_pixels):
            pixel_index = (i * 256 // num_pixels) + j
            color = wheel(pixel_index & 255)
            pixels_1[i] = color
            pixels_2[i] = color
            pixels_3[i] = color
        pixels_1.show()
        pixels_2.show()
        pixels_3.show()
        time.sleep(wait)

while True:
    # Fill both strips with red, green, and blue colors sequentially
    for color in [(255, 0, 0), (0, 255, 0), (0, 0, 255)]:
        pixels_1.fill(color)
        pixels_2.fill(color)
        pixels_3.fill(color)
        pixels_1.show()
        pixels_2.show()
        pixels_3.show()
        time.sleep(1)

    # Run a rainbow cycle on both strips simultaneously
    rainbow_cycle(0.001)
    
'''
pixels_1.fill((0,0,0))
pixels_2.fill((0,0,0))
pixels_3.fill((0,0,0))
pixels_1.show()
pixels_2.show()
pixels_3.show()
'''

