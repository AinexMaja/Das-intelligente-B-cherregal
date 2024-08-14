import time
from time import sleep
import RPi.GPIO as GPIO


# GPIO-Pin-Konfiguration
DIR = 20       # Richtungs-Pin
STEP = 21      # Schritt-Pin

CW = 1         # Uhrzeigersinn (rechts)
CCW = 0        # Gegen den Uhrzeigersinn (links)
SPR = 200       # Schritte pro Umdrehung

SWITCH_PIN_LEFT = 8   # Linker Limit-Switch Pin (normally closed)
SWITCH_PIN_RIGHT = 16 # Rechter Limit-Switch Pin (normally closed)

# Globale Variable für Motorposition
motor_position = 0
motor_position_cm = 0


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


# Motor bewegt sich nach rechts und links, ändert Richtung, wenn Limit Switch berührt wird
def move_motor(direction, speed):
    GPIO.output(DIR, direction)  # Richtung setzen
    while True:
        # Überprüfen, ob einer der Limit-Switches betätigt wurde
        if GPIO.input(SWITCH_PIN_LEFT) == GPIO.HIGH:
            print("Linker Limit-Switch aktiviert, Richtung ändern")
            sleep(1) # kurz warten
            direction = CCW if direction == CW else CW  # Richtung ändern
            GPIO.output(DIR, direction)  # Richtung setzen
            print("Motor bewegt sich nach", "rechts" if direction == CCW else "links")
            # kurzes Stück bewegen, damit Limit Sitch wieder deaktiviert ist
            for _ in range(20):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(0.001)
                GPIO.output(STEP, GPIO.LOW)
                sleep(0.001)
                # Position aktualisieren
                update_motor_position(direction, 1)  # 1 Schritt

        if GPIO.input(SWITCH_PIN_RIGHT) == GPIO.HIGH:
            print("Rechter Limit-Switch aktiviert, Richtung ändern")
            sleep(1)  # kurz warten
            direction = CCW if direction == CW else CW  # Richtung ändern
            GPIO.output(DIR, direction)  # Richtung setzen
            print("Motor bewegt sich nach", "rechts" if direction == CCW else "links")
            # kurzes Stück bewegen, damit Limit Sitch wieder deaktiviert ist
            for _ in range(20):
                GPIO.output(STEP, GPIO.HIGH)
                sleep(0.001)
                GPIO.output(STEP, GPIO.LOW)
                sleep(0.001)
                # Position aktualisieren
                update_motor_position(direction, 1)  # 1 Schritt
        
        # Bewegung, wenn kein Limit Switch gedrückt ist
        GPIO.output(STEP, GPIO.HIGH)
        sleep(0.1 / speed) 
        GPIO.output(STEP, GPIO.LOW)
        sleep(0.1 / speed)
        # Position aktualisieren
        update_motor_position(direction, 1)  # 1 Schritt

# Endlosschleife zum kontinuierlichen Hin- und Herfahren
try:
    direction = CW  # Start-Richtung (Rechts)
    speed = 100     # Geschwindigkeit (Schritte pro Sekunde)

    while True:
        print("Motor bewegt sich nach", "rechts" if direction == CCW else "links")
        move_motor(direction, speed)  # Bewege den Motor in die aktuelle Richtung

except KeyboardInterrupt:
    print("Programm unterbrochen")

finally:
    GPIO.cleanup()  # GPIO-Pins zurücksetzen