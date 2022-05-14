import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)
p = GPIO.PWM(36, 50)



try:
    p.start(5)
    while True:
        p.ChangeDutyCycle(5)  # extend
        time.sleep(3)
        p.ChangeDutyCycle(10)  # retract
        time.sleep(3)
except KeyboardInterrupt:
    p.stop()
    GPIO.cleanup()
