import time
import board
import neopixel
import threading
import numpy as np

# Define a list of colors to use for the LEDs
COLORS = [(255, 0, 0), (255, 0, 50), (255, 0, 255), (128, 0, 255), (0, 0, 255)]

# Pin configuration
pixel_pin = board.D12

# The number of NeoPixels
num_pixels = 300

# Define the color order of the NeoPixels (RGB or GRB)
ORDER = neopixel.GRB

# Initialize the NeoPixel strip
pixels = neopixel.NeoPixel(
    pixel_pin, num_pixels, brightness=0.2, auto_write=False, pixel_order=ORDER
)


# Flash LEDs at specified positions with given widths using different colors
def flashLED(positions, widths):
    # Convert single position/width to lists
    if type(positions) != type(np.array([])):
        positions = np.array([positions])
        widths = np.array([widths])
    color_idx = 0
    for position, width in zip(positions, widths):
        # Calculate the start and end indices for the LEDs to flash
        index1 = (position[0]+26.5)/0.625   # Our bookrow beginns at 26.5 cm of the LED strip
        index1 = int(index1)
        index2 = (position[0]+26.5+width[0])/0.625
        index2 = int(index2)

        # Set the color for each range of LEDs
        for i in range(index1, index2):
            pixels[i] = COLORS[color_idx]
        color_idx += 1
        if color_idx == len(COLORS):
            color_idx = 0
    # Update the LED strip with the new colors
    pixels.show()


# Turn off all the LEDs in the strip.
def clearLEDs():
    for i in range(len(pixels)):
        pixels[i] = (0, 0, 0)
        pixels.show()


# Run the both functions asynchronously in a separate thread.
def flashLED_async(positions, widths):
    thread = threading.Thread(target=flashLED, args=(positions, widths))
    thread.start()

def clearLEDs_async():
    thread = threading.Thread(target=clearLEDs)
    thread.start()        
