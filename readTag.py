# This code reads  RFID tas and prints the RFID ID to the 
# command line. These RFID IDs will then be associated with 
# a specific song.

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

while(True):
    try:
        id = reader.read()[0]
        print("tag ID:", id)
            
    finally:
        GPIO.cleanup()