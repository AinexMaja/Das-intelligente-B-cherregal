import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
SWITCH_PIN = 8
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    while True:
        if GPIO.input(SWITCH_PIN) == GPIO.HIGH:
            print("The limit switch is TOUCHED")
        else:
            print("The limit switch is UNTOUCHED")
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()