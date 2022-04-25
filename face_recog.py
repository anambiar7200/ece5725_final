import face_recognition
import cv2
import numpy as np
import time

img_alisha = face_recognition.load_image_file('/home/pi/ece5725_final/test.jpg')
img_alisha_encoding = face_recognition.face_encodings(img_alisha)[0]

known_face_encodings = [img_alisha_encoding]
known_face_names = ["Alisha"]
