import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
p = GPIO.PWM(15, 50)

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
