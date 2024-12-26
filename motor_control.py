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


# calculate the distance for the stepper motor to move
def calculate_distance(position_in_cm):
    global motor_position
    # move stepper motor to the left after starting the program
    if motor_position < 0:
        return float("-10000")
    position_in_steps = int(position_in_cm * SPR)
    #error correction
    position_in_steps /= 0.961
    new_position = position_in_steps - motor_position
    return new_position

# def push_book(speed):
#     while (GPIO.input(DC_MOTOR_SWITCH) == UNTOUCHED):
#         GPIO.output(DC_MOTOR_EXTEND, 0)
#         GPIO.output(DC_MOTOR_RETRACT, 1)
#     print(GPIO.input(DC_MOTOR_SWITCH))
#     GPIO.output(DC_MOTOR_RETRACT, 0)
#     GPIO.output(DC_MOTOR_EXTEND, 1)
#     sleep(4.3)
#     while GPIO.input(DC_MOTOR_SWITCH) == UNTOUCHED:
#         GPIO.output(DC_MOTOR_EXTEND, 0)
#         GPIO.output(DC_MOTOR_RETRACT, 1)
#     GPIO.output(DC_MOTOR_EXTEND, 0)
#     GPIO.output(DC_MOTOR_RETRACT, 0)

def push_book(speed=1):
    GPIO.output(ENABLE_EXTENDER, 0)
    sleeptime = 0.05
    for direction in [CW, CCW, CW]:
        GPIO.output(DIR, direction)
        for i in range(30):
            if GPIO.input(DC_MOTOR_SWITCH) == TOUCHED:
                break
            GPIO.output(STEP, GPIO.HIGH)
            sleep(sleeptime)
            GPIO.output(STEP, GPIO.LOW)
            sleep(sleeptime)
    GPIO.output(ENABLE_EXTENDER, 1)


def move(book_center, speed):
    global motor_position
    calibration = motor_position < 0
    for position in book_center:
        distance = calculate_distance(position)
        print("distance", distance)

        if distance > 0:
            distance = distance
            direction = CCW
        elif distance < 0:
            distance = -distance  
            direction = CW

        GPIO.output(ENABLE_RAIL, 0)
        GPIO.output(DIR, direction)

        steps = distance
        speedup_slowdown = "speedup"
        for _ in range(2):
            for step in range(int(steps/2)):
                # check limit switches
                if GPIO.input(SWITCH_PIN_LEFT) == TOUCHED and direction == CW:
                    motor_position = 0
                    print("Linker Limit-Switch aktiviert, Bewegung gestoppt!")
                    break

                if GPIO.input(SWITCH_PIN_RIGHT) == TOUCHED and direction == CCW:
                    motor_position = 2663
                    print("Rechter Limit-Switch aktiviert, Bewegung gestoppt!")
                    break
                
                if speedup_slowdown == "speedup":
                    x = step
                elif speedup_slowdown == "slowdown":
                    x = abs(step - int(steps/2))

                # move stepper motor    
                GPIO.output(STEP, GPIO.HIGH)
                sleeptime = max(0.000447, abs(sqrt(x) - sqrt(x+1))/speed)
                sleep(sleeptime)
                GPIO.output(STEP, GPIO.LOW)
                sleep(sleeptime)
                if direction == 0:
                    motor_position += 1
                elif direction == 1:
                    motor_position -= 1
                print("Motorposition: " + str(motor_position))
            speedup_slowdown = "slowdown"
        if not calibration:
            push_book(PUSH_SPEED)
    GPIO.output(ENABLE_RAIL, 1)

def move_async(book_center, speed):
    thread = threading.Thread(target=move, args=(book_center, speed))
    thread.start()

move([0], 50)
push_book()