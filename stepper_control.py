from time import sleep
import RPi.GPIO as GPIO
from math import sqrt

DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
ENABLE = 16 # Enable GPIO Pin

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENABLE, GPIO.OUT)
GPIO.output(DIR, CW)

# step_count = 900
# #delay = .0005
# delay = 0.5

# for x in range(step_count):
#     GPIO.output(STEP, GPIO.HIGH)
#     sleep(delay)
#     GPIO.output(STEP, GPIO.LOW)
#     sleep(delay)

# sleep(.5)
# GPIO.output(DIR, CCW)
# for x in range(step_count):
#     GPIO.output(STEP, GPIO.HIGH)
#     sleep(delay)
#     GPIO.output(STEP, GPIO.LOW)
#     sleep(delay)

def move(distance, direction, speed):
    GPIO.output(ENABLE, 0)
    # distance /= 0.96
    GPIO.output(DIR, direction)
    steps = int(distance * SPR)
    for step in range(int(steps/2)):
        x = step
        print(abs(sqrt(x) - sqrt(x+1))/speed)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(abs(sqrt(x) - sqrt(x+1))/speed)
        GPIO.output(STEP, GPIO.LOW)
        sleep(abs(sqrt(x) - sqrt(x+1))/speed)
    for step in range(int(steps/2)):
        x = abs(step - int(steps/2))
        print(abs(sqrt(x) - sqrt(x+1))/speed)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(abs(sqrt(x) - sqrt(x+1))/speed)
        GPIO.output(STEP, GPIO.LOW)
        sleep(abs(sqrt(x) - sqrt(x+1))/speed)
    GPIO.output(ENABLE, 1)

move(2, 0, 50)
sleep(1)
for _ in range(1):
    move(50, 0, 50)
    sleep(1)
    move(50, 1, 50)
    sleep(1)

# sudGPIO.cleanup()
# GPIO.setup(ENABLE, GPIO.OUT)
# GPIO.output(ENABLE, 1)