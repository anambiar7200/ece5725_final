import face_recognition as fr
import cv2
import numpy as np
import os
import pickle

def get_encodings(usr):
    known_names = []
    known_name_encodings = []
    
    path = "./pictures/" + str(usr) 
    images = os.listdir(path)
    for _ in images:
        image = fr.load_image_file(path +"/" + _)

        image_path = path + "/" + _
        #print(image_path)
        encoding = fr.face_encodings(image)[0]
        #print(encoding)

        known_name_encodings.append(encoding)
        known_names.append(usr)
    
    with open("encodings", "ab") as enc: 
        pickle.dump(known_name_encodings, enc)
    with open("names", "ab") as names: 
        pickle.dump(known_names, names)



#test_image = "./test/test.jpg"
test_image = "anusha1.png"
#test_image = "alisha1.jpg"

def test_recog(test_image,true_name):
    known_names = []
    with open("names", "rb") as names: 
        try: 
            while True: 
                known_names+= pickle.load(names)
        except EOFError: 
            print("here")
            
    known_name_encodings = []        
    with open("encodings", "rb") as enc: 
        try: 
            while True: 
                known_name_encodings += pickle.load(enc)
        except EOFError: 
            pass
            
            
            
    #with open("encodings", "rb") as enc: 
    #    known_name_encodings = pickle.load(enc)
    #with open("names", "rb") as names: 
    #    known_names = pickle.load(names)
    image = cv2.imread(test_image)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_locations = fr.face_locations(image)
    face_encodings = fr.face_encodings(image, face_locations)
    
    name = ""
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = fr.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = fr.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)

        if matches[best_match]:
            name = known_names[best_match]

        #cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        #cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
        #font = cv2.FONT_HERSHEY_DUPLEX
        #cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    # cv2.imshow("Result", image)
    # cv2.imwrite("./output.jpg", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return name == true_name
#get_encodings("user2")
#encode = input("Do you need to get encodings?")
#if encode == "yes": 
#    get_encodings("user1")
#    get_encodings("user2")
#users = ["user1", "user2"]
#for usr in users: 
#    get_encodings(usr)
#print(test_recog(test_image,  "user2"))
