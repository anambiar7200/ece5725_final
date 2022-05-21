""" Anusha Nambiar (aan29), Alisha Kochar (ak225)
    ECE 5725 Final 
    Spring 2022
"""
"""
	Script we used to test writing to the RFID tags.
"""
from pirc522 import RFID
import signal
import time
from datetime import datetime

rdr = RFID(1, 0, 1000000, 31, 37, 29)
util = rdr.util()
# Set util debug to true - it will print what's going on
util.debug = True


# Wait for tag
rdr.wait_for_tag()

# Request tag
(error, data) = rdr.request()
if not error:
    print("\nDetected")

    (error, uid) = rdr.anticoll()
    if not error:
        # Print UID
        print("Card read UID: "+str(uid[0])+","+str(uid[1])+","+str(uid[2])+","+str(uid[3]))

        # Set tag as used in util. This will call RFID.select_tag(uid)
        util.set_tag(uid)
        util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])
        util.read_out(4)
        
        x = datetime.now()
        print(x)
        data = [x.year%2000, x.month, x.day, x.hour, x.minute, x.second]
        
        util.rewrite(9, data)
        util.read_out(9)
    
