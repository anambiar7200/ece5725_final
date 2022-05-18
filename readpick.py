import pickle
data = []
with open("names", "rb") as names: 
	try: 
		while True: 
			data.append(pickle.load(names))
	except EOFError: 
		print("here")

print(data)
