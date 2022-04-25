from deepface import DeepFace

img1 = "anusha1.png"
img2 = "anusha2.png"


camera = PiCamera()

camera.start_preview()
time.sleep(2)

camera.capture("test.jpg")


model_name = "Facenet"

resp = DeepFace.verify(img1_path= img1, img2_path = "test.jpg", model_name = model_name)

print(resp)

