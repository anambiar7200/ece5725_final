import face_recognition as fr
import cv2
import numpy as np
import os
import pickle

encodings = []

def get_encodings(usr): 
    path = "./pictures/" + str(usr) 
    images = os.listdir(path)

    # if usr not in encodings:
    #   encodings[usr] = []
    
    for _ in images: 
      image = fr.load_image_file(path +"/" + _)

      image_path = path + "/" + _
      print(image_path)
      encoding = fr.face_encodings(image)[0]

      encodings.append((encoding, usr))

    with open("encodings", "ab") as enc: 
        pickle.dump(encodings, enc)

def test_recog(test_image,true_name):
  image = cv2.imread(test_image)

  face_locations = fr.face_locations(image)
  face_encodings = fr.face_encodings(image, face_locations)

  with open("encodings", "rb") as enc: 
    encodings = pickle.load(enc)

  known_name_encodings = [x[0] for x in encodings]
  known_names = [x[1] for x in encodings]
  
  name = ""
  for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
      matches = fr.compare_faces(known_name_encodings, face_encoding)
      name = ""

      face_distances = fr.face_distance(known_name_encodings, face_encoding)
      best_match = np.argmin(face_distances)

      if matches[best_match]:
          name = known_names[best_match]
  return name == true_name

def del_encodings(uname): 
  with open("encodings", "rb") as enc: 
    encodings = pickle.load(enc)

  output = [(encoding, usr) for encoding,usr in encodings if (usr != uname)]

  with open("encodings", "ab") as enc: 
        pickle.dump(output, enc)


