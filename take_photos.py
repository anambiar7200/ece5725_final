import cv2
import io
#import picamera
import numpy
import keyboard
import os

user_num = 2

# stream = io.BytesIO()

# with picamera.PiCamera() as camera: 
# 	camera.resolution = (320, 240)
# 	camera.capture(stream, format='jpeg')

img_taken = 0
total_num_img = 3

dirname = "user" + str(user_num)
if dirname not in os.listdir("pictures"):
  os.mkdir("pictures" + dirname)
  existing_pics = 0
else: 
  existing_pics = len(os.listdir("pictures/"+dirname))


while (img_taken < total_num_img): 
  cam = cv2.VideoCapture(0)
  rect, img = cam.read()
  flname = "pictures/" + dirname + "/pic" + str(img_taken + existing_pics) + ".jpg"
  print(flname)
  cv2.imwrite(flname, img)
  img_taken += 1