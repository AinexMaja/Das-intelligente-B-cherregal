import RPi.GPIO as GPIO
from time import sleep
from math import sqrt
import threading


# Pin configuration
DIR = 20   # Direction GPIO pin
STEP = 21  # Step GPIO pin
ENABLE = 16 # Enable GPIO pin

CW = 1     # Clockwise rotation
CCW = 0    # Counterclockwise rotation
SPR = 48   # Steps per revolution (360 / 7.5)

# Limit switches
SWITCH_PIN_LEFT = 26   # Left limit switch pin
SWITCH_PIN_RIGHT = 8 # Right limit switch pin
DC_MOTOR_SWITCH = 17 # Middle limit switch pin
UNTOUCHED = GPIO.LOW
TOUCHED = GPIO.HIGH

# DC motor
DC_MOTOR_EXTEND = 13
DC_MOTOR_RETRACT = 18
PUSH_SPEED = 1

motor_position = -1 # (in steps) Variable, that tracks the motor position (-1 indicates uncalibrated)

# GPIO configuration for RPi
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENABLE, GPIO.OUT)
GPIO.setup(DC_MOTOR_EXTEND, GPIO.OUT)
GPIO.setup(DC_MOTOR_RETRACT, GPIO.OUT)
GPIO.setup(SWITCH_PIN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Pull-up for Limit-Switch
GPIO.setup(SWITCH_PIN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull-up for Limit-Switch
GPIO.setup(DC_MOTOR_SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_UP) # Pull-up for Limit-Switch


# calculate the distance for the stepper motor to move
def calculate_distance(position_in_cm):
    global motor_position
    # move stepper motor to the left after starting the program
    if motor_position < 0:
        return float("-10000") # movement to the left
    position_in_steps = int(position_in_cm * SPR)
    # error correction
    position_in_steps /= 0.961
    new_position = position_in_steps - motor_position
    return new_position

def push_book(speed):
    # Retract the DC motor until the limit switch is pressed
    while (GPIO.input(DC_MOTOR_SWITCH) == UNTOUCHED):
        GPIO.output(DC_MOTOR_EXTEND, 0)
        GPIO.output(DC_MOTOR_RETRACT, 1)
    # Extend the DC motor for 4.3 seconds
    GPIO.output(DC_MOTOR_RETRACT, 0)
    GPIO.output(DC_MOTOR_EXTEND, 1)
    sleep(4.3)
    # Retract the DC motor back until the limit switch is pressed
    while GPIO.input(DC_MOTOR_SWITCH) == UNTOUCHED:
        GPIO.output(DC_MOTOR_EXTEND, 0)
        GPIO.output(DC_MOTOR_RETRACT, 1)
    # stop movement
    GPIO.output(DC_MOTOR_EXTEND, 0)
    GPIO.output(DC_MOTOR_RETRACT, 0)

# move stepper motor to the desired position
def move(book_center, speed):
    global motor_position
    calibration = motor_position < 0  # Check if motor is in calibration mode
    for position in book_center:
        distance = calculate_distance(position)

        # Determine the direction
        if distance > 0:
            distance = distance
            direction = CCW
        elif distance < 0:
            distance = -distance  
            direction = CW

        GPIO.output(ENABLE, 0)
        GPIO.output(DIR, direction)

        # Move the motor the calculated number of steps with speed ramping
        steps = distance
        speedup_slowdown = "speedup"
        for _ in range(2):  # Speed up for the first half, slow down for the second half
            for step in range(int(steps/2)):
                # check limit switches (to stop the motor if triggered)
                if GPIO.input(SWITCH_PIN_LEFT) == TOUCHED and direction == CW:
                    motor_position = 0  # Set the motor position to the leftmost point
                    print("Linker Limit-Switch aktiviert, Bewegung gestoppt!")
                    break

                if GPIO.input(SWITCH_PIN_RIGHT) == TOUCHED and direction == CCW:
                    motor_position = 2663  # Set the motor position to the rightmost point
                    print("Rechter Limit-Switch aktiviert, Bewegung gestoppt!")
                    break
                
                 # Speed ramping logic
                if speedup_slowdown == "speedup":
                    x = step
                elif speedup_slowdown == "slowdown":
                    x = abs(step - int(steps/2))

                # move stepper motor    
                GPIO.output(STEP, GPIO.HIGH)
                sleeptime = max(0.000447, abs(sqrt(x) - sqrt(x+1))/speed)  # Calculate step timing
                sleep(sleeptime)
                GPIO.output(STEP, GPIO.LOW)
                sleep(sleeptime)
                if direction == 0:
                    motor_position += 1
                elif direction == 1:
                    motor_position -= 1
            speedup_slowdown = "slowdown"  # Switch to slowdown phase for the second half of movement
        # Push the book after the motor reaches its position    
        if not calibration:
            push_book(PUSH_SPEED)
    GPIO.output(ENABLE, 1)

# Asynchronous version of the move function
def move_async(book_center, speed):
    thread = threading.Thread(target=move, args=(book_center, speed))
    thread.start()