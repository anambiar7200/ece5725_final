import cv2
import io
import picamera
import numpy


stream = io.BytesIO()

with picamera.PiCamera() as camera: 
	camera.resolution = (320, 240)
	camera.capture(stream, format='jpeg')


haar_path = (cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cascade = cv2.CascadeClassifier(haar_path)

img = cv2.imdecode(numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8), 1)
gray_img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


faces = cascade.detectMultiScale(gray_img, 1.1, 5)


#Draw a rectangle around every found face
for (x,y,w,h) in faces:
	print("found a face")
	cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),4)

cv2.imwrite('result.jpg',img)
#cv2.imshow("result", img)
    
  # Wait for Esc key to stop
#  k = cv2.waitKey(30) & 0xff
#  if k == 27:
#      break
    
# Close the window
#cap.release()
