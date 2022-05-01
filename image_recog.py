from deepface import DeepFace
import cv2

img1 = "anusha1.png"
img2 = "anusha2.png"


camera = PiCamera()

camera.start_preview()
time.sleep(2)

camera.capture("test.jpg")
