""" Anusha Nambiar (aan29), Alisha Kochar (ak225)
    ECE 5725 Final 
    Spring 2022
"""
"""
	Module containing the function take_pics(user_num) which takes
  50 pictures of user_num and saves them to ./pictures/userN
"""
import cv2
import io
import picamera
import numpy
import os

def take_pics(user_num):
  stream = io.BytesIO()

  with picamera.PiCamera() as camera: 
    camera.resolution = (320, 240)
    camera.capture(stream, format='jpeg')
    
  img_taken = 0
  total_num_img = 50

  dirname = "user" + str(user_num)
  if dirname not in os.listdir("pictures"):
    os.mkdir("pictures/" + dirname)
    existing_pics = 0
  else: 
    existing_pics = len(os.listdir("pictures/"+dirname))


  while (img_taken < total_num_img): 
    img = cv2.imdecode(numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8), 1)
    flname = "pictures/" + dirname + "/pic" + str(img_taken + existing_pics) + ".jpg"
    cv2.imwrite(flname, img)
    img_taken += 1
