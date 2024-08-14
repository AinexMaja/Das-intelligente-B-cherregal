import time
from time import sleep
import RPi.GPIO as GPIO

# GPIO-Pin-Konfiguration
DIR = 20       # Richtungs-Pin
STEP = 21      # Schritt-Pin

CW = 1         # Uhrzeigersinn (rechts)
CCW = 0        # Gegen den Uhrzeigersinn (links)
SPR = 200      # Schritte pro Umdrehung
DIST_PER_REV_CM = 48.7  # Distanz pro Umdrehung in cm (abhängig von der Mechanik)

# Berechnung der Umrechnung von Schritten in cm
CM_PER_STEP = DIST_PER_REV_CM / SPR

SWITCH_PIN_LEFT = 8   # Linker Limit-Switch Pin (normally closed)
SWITCH_PIN_RIGHT = 16 # Rechter Limit-Switch Pin (normally closed)

# Globale Variable für Motorposition in cm
motor_position_cm = 0
motor_position = 0

# GPIO-Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(SWITCH_PIN_LEFT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SWITCH_PIN_RIGHT, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# Motorposition aktualisieren
def update_motor_position(direction, steps):
    global motor_position_cm
    global motor_position
    if direction == CW:
        motor_position -= steps
        motor_position_cm = motor_position/48,25
    elif direction == CCW:
        motor_position += steps
        motor_position_cm = motor_position/48,25
    # Motorposition in cm ausgeben
    print("Motorposition: " + str(motor_position_cm) + "cm")


# Motor bewegen bis zur gewünschten Position
def move_to_position(target_cm, speed):
    global motor_position_cm
    target_steps = int(target_cm / CM_PER_STEP)
    direction = CW if target_cm < motor_position_cm else CCW
    GPIO.output(DIR, direction)  # Richtung setzen

    while True:
        # Überprüfen, ob ein Limit-Switch betätigt wurde
        if GPIO.input(SWITCH_PIN_LEFT) == GPIO.HIGH:
            print("Linker Limit-Switch aktiviert, Richtung ändern")
            direction = CCW
            GPIO.output(DIR, direction)
            # Kurzes Stück bewegen
            for _ in range(20):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(0.001)
                GPIO.output(STEP, GPIO.LOW)
                sleep(0.001)
                update_motor_position(direction, 1)

        if GPIO.input(SWITCH_PIN_RIGHT) == GPIO.HIGH:
            print("Rechter Limit-Switch aktiviert, Richtung ändern")
            direction = CW
            GPIO.output(DIR, direction)
            # Kurzes Stück bewegen
            for _ in range(20):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(0.001)
                GPIO.output(STEP, GPIO.LOW)
                sleep(0.001)
                update_motor_position(direction, 1)
        
        # Schritt ausführen
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.1 / speed)
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.1 / speed)
        update_motor_position(direction, 1)
        
        # Überprüfen, ob das Ziel erreicht wurde
        if direction == CW and motor_position_cm <= target_cm:
            break
        elif direction == CCW and motor_position_cm >= target_cm:
            break

# Benutzer zur Eingabe der Zielposition auffordern
try:
    speed = 100  # Geschwindigkeit (Schritte pro Sekunde)

    while True:
        target_cm = float(input("Gib die Zielposition in cm ein (oder 'q' zum Beenden): "))
        move_to_position(target_cm, speed)

except KeyboardInterrupt:
    print("Programm unterbrochen")

finally:
    GPIO.cleanup()  # GPIO-Pins zurücksetzen