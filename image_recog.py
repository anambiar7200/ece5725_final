import cv2


#stream = io.ByestIO()

# with picamera.PiCamera() as camera: 
#   camera.capture(stream, format='jpeg')
haar_path = (cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
cascade = cv2.CascadeClassifier(haar_path)

#img = cv2.imdecode(numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8, 1)
capture = cv2.VideoCapture(0)

while True: 
  rect, img = capture.read()
  gray_img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = cascade.detectMultiScale(gray_img, 1.3, 5)


  #Draw a rectangle around every found face
  for (x,y,w,h) in faces:
      cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),4)

  cv2.imshow('img',img)
    
  # Wait for Esc key to stop
  k = cv2.waitKey(30) & 0xff
  if k == 27:
      break
    
# Close the window
cap.release()