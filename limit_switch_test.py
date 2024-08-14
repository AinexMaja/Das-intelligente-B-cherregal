import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SWITCH_PIN = 16
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(SWITCH_PIN) == GPIO.LOW:
            print("The limit switch is UNTOUCHED")
        else:
            print("The limit switch is TOUCHED")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()