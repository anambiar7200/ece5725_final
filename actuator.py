import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
p = GPIO.PWM(18, 50)

p.start(5)

try:
    while True:
        p.ChangeDutyCycle(5)  # extend
        time.sleep(3)
        p.ChangeDutyCycle(10)  # retract
        time.sleep(3)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()