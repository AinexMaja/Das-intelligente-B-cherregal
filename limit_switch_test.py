import RPi.GPIO as GPIO
import time
from time import sleep

GPIO.setmode(GPIO.BCM)
SWITCH_PIN = 17
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

DC_MOTOR_EXTEND = 13
DC_MOTOR_RETRACT = 18
GPIO.setup(DC_MOTOR_EXTEND, GPIO.OUT)
GPIO.setup(DC_MOTOR_RETRACT, GPIO.OUT)

try:
    # while True:
    #     if GPIO.input(SWITCH_PIN) == GPIO.HIGH:
    #         print("The limit switch is TOUCHED")
    #     if GPIO.input(SWITCH_PIN) == GPIO.LOW:
    #         print("The limit switch is UNTOUCHED")
    while True:
        GPIO.output(DC_MOTOR_EXTEND, 0)
        GPIO.output(DC_MOTOR_RETRACT, 1)
        while GPIO.input(SWITCH_PIN) == GPIO.HIGH:
            pass
        print("Switched to Low state")
        GPIO.output(DC_MOTOR_RETRACT, 0)
        GPIO.output(DC_MOTOR_EXTEND, 1)
        while GPIO.input(SWITCH_PIN) == GPIO.LOW:
            pass
        print(time.time() ,"Switched to High state")
except KeyboardInterrupt:
    GPIO.cleanup()