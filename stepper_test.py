from time import sleep
import RPi.GPIO as GPIO

# GPIO-Pins definieren
DIR = 20    # Richtungs-Pin
STEP = 21   # Schritt-Pin
ENABLE = 16 # Aktivierungs-Pin

# Drehrichtung definieren
CW = 1  # 1 = Schlitten nach links, 0 = Schlitten nach rechts

# Schritte pro Umdrehung (abhängig von deinem Motor)
SPR = 48  # Zum Beispiel 48 Schritte pro Umdrehung

# GPIO-Modus festlegen
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(ENABLE, GPIO.OUT)

# Richtung auf Uhrzeigersinn setzen
GPIO.output(DIR, CW)

# Aktivierung des Motors
GPIO.output(ENABLE, 0)

# Anzahl der Schritte, die der Motor sich bewegen soll (z.B. 20 Schritte)
step_count = 10

# Verzögerung zwischen den Schritten (kann angepasst werden)
delay = 0.001  # 10ms

# Motor bewegen
for _ in range(step_count):
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

# Motor deaktivieren
GPIO.output(ENABLE, 1)

# GPIO-Säuberung (optional)
GPIO.cleanup()