from time import sleep
import RPi.GPIO as GPIO
from math import sqrt


DIR = 20   # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
ENABLE = 16 # Enable GPIO Pin

CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 48   # Steps per Revolution (360 / 7.5)

SWITCH_PIN_LEFT = 26   # Left Limit-Switch pin
SWITCH_PIN_RIGHT = 8 # Right Limit-Switch pin

motor_position = 0 # (in steps)


GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENABLE, GPIO.OUT)
GPIO.output(DIR, CW)

GPIO.setup(SWITCH_PIN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up for Limit-Switch
GPIO.setup(SWITCH_PIN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull-up for Limit-Switch


def calculate_distance(position_in_cm):
    global motor_position
    position_in_steps = int(position_in_cm * SPR)
    position_in_steps /= 0.961
    new_position = motor_position - position_in_steps
    if new_position > 0:
        new_position = new_position
        direction = CW
    elif new_position < 0:
        new_position = -new_position    
        direction = CCW
    return (new_position, direction)


def move(distance, direction, speed):
    global motor_position
    GPIO.output(ENABLE, 0)
    GPIO.output(DIR, direction)
    steps = distance
    speedup_slowdown = "speedup"
    for _ in range(2):
        for step in range(int(steps/2)):
            # check limit switches
            if GPIO.input(SWITCH_PIN_LEFT) == GPIO.HIGH and direction == CW:
                motor_position = 0
                print("Linker Limit-Switch aktiviert, Bewegung gestoppt!")
                break

            if GPIO.input(SWITCH_PIN_RIGHT) == GPIO.HIGH and direction == CCW:
                motor_position = 2663
                print("Rechter Limit-Switch aktiviert, Bewegung gestoppt!")
                break
            
            if speedup_slowdown == "speedup":
                x = step
            elif speedup_slowdown == "slowdown":
                x = abs(step - int(steps/2))
            #print(abs(sqrt(x) - sqrt(x+1))/speed)
            GPIO.output(STEP, GPIO.HIGH)
            sleep(abs(sqrt(x) - sqrt(x+1))/speed)
            GPIO.output(STEP, GPIO.LOW)
            sleep(abs(sqrt(x) - sqrt(x+1))/speed)
            if direction == 0:
                motor_position += 1
            elif direction == 1:
                motor_position -= 1
            print("Motorposition: " + str(motor_position))
        speedup_slowdown = "slowdown"
    GPIO.output(ENABLE, 1)


move(500, 1, 50)
sleep(1)

# sudGPIO.cleanup()
# GPIO.setup(ENABLE, GPIO.OUT)
# GPIO.output(ENABLE, 1)