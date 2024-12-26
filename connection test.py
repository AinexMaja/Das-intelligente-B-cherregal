from time import sleep
import RPi.GPIO as GPIO
from math import sqrt
import threading


DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
ENABLE_RAIL = 16 # ENABLE_RAIL GPIO Pin
ENABLE_EXTENDER = 13

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)

SWITCH_PIN_LEFT = 26   # Left Limit-Switch pin
SWITCH_PIN_RIGHT = 8 # Right Limit-Switch pin
DC_MOTOR_SWITCH = 17 # Middle Limit-Switch pin

motor_position = -1 # (in steps)

# DC_MOTOR_EXTEND = 13
# DC_MOTOR_RETRACT = 18

PUSH_SPEED = 1
UNTOUCHED = GPIO.LOW
TOUCHED = GPIO.HIGH

# GPIO configuration
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENABLE_RAIL, GPIO.OUT)
GPIO.setup(ENABLE_EXTENDER, GPIO.OUT)
# GPIO.setup(DC_MOTOR_EXTEND, GPIO.OUT)
# GPIO.setup(DC_MOTOR_RETRACT, GPIO.OUT)
GPIO.setup(SWITCH_PIN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up for Limit-Switch
GPIO.setup(SWITCH_PIN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull-up for Limit-Switch
GPIO.setup(DC_MOTOR_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull-up for Limit-Switch

GPIO.output(ENABLE_EXTENDER, 1)
GPIO.output(ENABLE_RAIL, 1)
while True:
    GPIO.output(STEP, 1)
    sleep(0.1)
    GPIO.output(STEP, 0)
    sleep(0.1)