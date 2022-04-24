from deepface import DeepFace

img1 = "anusha1.png"
img2 = 'anusha2.png'
model_name = "Facenet"

resp = DeepFace.verify(img1_path = img1, img2_path = img2, model_name = model_name)