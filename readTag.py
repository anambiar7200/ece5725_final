# This code reads  RFID tas and prints the RFID ID to the 
# command line. These RFID IDs will then be associated with 
# a specific individual.

# import RPi.GPIO as GPIO
# from mfrc522 import SimpleMFRC522

# reader = SimpleMFRC522()

# while(True):
#     try:
#         id = reader.read()[0]
#         print("tag ID:", id)
            
#     finally:
#         GPIO.cleanup()

import RPi.GPIO as GPIO
from pirc522 import RFID

rdr = RFID(1, 0, 1000000, 31, 37, 29)
print("before while loop")

while True:
  print("waiting for tag")
  rdr.wait_for_tag()
  (error, tag_type) = rdr.request()
  if not error:
    print("Tag detected")
    (error, uid) = rdr.anticoll()
    if not error:
      print("UID: " + str(uid))
      # Select Tag is required before Auth
      if not rdr.select_tag(uid):
        # Auth for block 10 (block 2 of sector 2) using default shipping key A
        if not rdr.card_auth(rdr.auth_a, 10, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], uid):
          # This will print something like (False, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
          print("Reading block 10: " + str(rdr.read(10)))
          # Always stop crypto1 when done working
          rdr.stop_crypto()

# Calls GPIO cleanup
rdr.cleanup()
