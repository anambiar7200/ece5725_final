import RPI.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)

motor1A=16
# motor1B=18
# motor1E=22

GPIO.setup(motor1A, GPIO.OUT)
# GPIO.setup(motor1B, GPIO.OUT)
# GPIO.setup(motor1E, GPIO.OUT)

print("turning motor on")
GPIO.output(motor1A, GPIO.HIGH)
# GPIO.output(motor1B, GPIO.LOW)
# GPIO.output(motor1E, GPIO.HIGH)

# sleep(10.16)

# ratio = input("Enter desired stretch ratio (decimal)")
# length = input("Enter sample length (mm)")
# variable = (((ratio))*((length))*.01)

# print("begin tissue stretch")
# GPIO.output(motor1A, GPIO.LOW)
# GPIO.output(motor1B, GPIO.HIGH)
# GPIO.output(motor1E, GPIO.HIGH)

# sleep(variable)

# print("end of tissue stretch")
# GPIO.output(motor1E, GPIO.LOW)

# GPIO.cleanup()