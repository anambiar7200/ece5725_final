""" Anusha Nambiar (aan29), Alisha Kochar (ak225)
    ECE 5725 Final 
    Spring 2022
"""
"""
    Module containing the facial recognition functions
    get_encodings and test_recog used in read.py 
"""

import face_recognition as fr
import cv2
import numpy as np
import os
import pickle

# Function that gets the face encodings of all the 
# photos in ./pictures/usr
# Write encodings to "encodings" and names to "names"
def get_encodings(usr):
    known_names = []
    known_name_encodings = []
    
    path = "./pictures/" + str(usr) 
    images = os.listdir(path)
    for _ in images:
        image = fr.load_image_file(path +"/" + _)

        image_path = path + "/" + _
        encoding = fr.face_encodings(image)[0]

        known_name_encodings.append(encoding)
        known_names.append(usr)
    
    with open("encodings", "ab") as enc: 
        pickle.dump(known_name_encodings, enc)
    with open("names", "ab") as names: 
        pickle.dump(known_names, names)



#test_image = "./test/test.jpg"
#test_image = "anusha1.png"
#test_image = "alisha1.jpg"

# Function that tests whether or not the face in test_image matches true_name
def test_recog(test_image,true_name):
    # Get names and encodings
    known_names = []
    with open("names", "rb") as names: 
        try: 
            while True: 
                known_names+= pickle.load(names)
        except EOFError: 
            pass
            
    known_name_encodings = []        
    with open("encodings", "rb") as enc: 
        try: 
            while True: 
                known_name_encodings += pickle.load(enc)
        except EOFError: 
            pass

    # Read in the test image
    image = cv2.imread(test_image)

    # Find the face and get the encoding from test image
    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)
    
    # Loop through the encodings and return the name of the one that 
    # best matches (least face_distance) the test image
    name = ""
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)

        if matches[best_match]:
            name = known_names[best_match]
    # Return wether or not the best match name is the same as the expected name
    return name == true_name

