import sys
sys.path.append("/usr/lib/python3/dist-packages")
from picamera import PiCamera
import time

camera = PiCamera()

camera.start_preview()
time.sleep(2)

camera.capture("test.jpg")
