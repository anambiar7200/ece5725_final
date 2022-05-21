""" Anusha Nambiar (aan29), Alisha Kochar (ak225)
    ECE 5725 Final 
    Spring 2022
"""
"""
	Unused script that took an image and drew rectangles around the faces.
"""
import cv2
import io
import picamera
import numpy

# Start a stream
stream = io.BytesIO()

# Take a photo
with picamera.PiCamera() as camera: 
	camera.resolution = (320, 240)
	camera.capture(stream, format='jpeg')

# Get the Haar cascade classifier
haar_path = (cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cascade = cv2.CascadeClassifier(haar_path)

# Get the image decode and convert to grayscale
img = cv2.imdecode(numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8), 1)
gray_img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Get a list of all the faces
faces = cascade.detectMultiScale(gray_img, 1.1, 5)


#Draw a rectangle around every found face
for (x,y,w,h) in faces:
	print("found a face")
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),4)

# Output the result to 'result.jpg'
cv2.imwrite('result.jpg',img)
