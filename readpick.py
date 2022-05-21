""" Anusha Nambiar (aan29), Alisha Kochar (ak225)
    ECE 5725 Final 
    Spring 2022
"""
"""
	Script we used to test reading Pickled files; incorporated
	into read.py and face_recog.py
"""

import pickle
data = []
with open("names", "rb") as names: 
	try: 
		while True: 
			data.append(pickle.load(names))
	except EOFError: 
		#print("here")

print(data)
