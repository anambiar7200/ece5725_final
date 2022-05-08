import sys
sys.path.append("/usr/lib/python3/dist-packages")
import picamera 
import cv2
import time
import RPi.GPIO as GPIO
from pirc522 import RFID
import pygame
from pygame.locals import * 
import os
import subprocess
import io
import numpy
from datetime import datetime
import face_recog as fr

#os.putenv("SDL_VIDEODRIVER","fbcon")
#os.putenv("SDL_FBDEV", "/dev/fb0")
#os.putenv("SDL_MOUSEDRV", "TSLIB")
#os.putenv("SDL_MOUSEDEV", "/dev/input/touchscreen")

#start_time = time.time() 
#GPIO.setmode(GPIO.BOARD)

pygame.init()
WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255, 0, 0
GREEN = 0, 255, 0
screen = pygame.display.set_mode((320, 240))
my_font = pygame.font.Font(None, 30)
my_small_font = pygame.font.Font(None, 20)
pygame.mouse.set_visible(True)

rdr = RFID(1, 0, 1000000, 31, 37, 29)
util = rdr.util()
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)

anusha = [194, 238, 139, 27, 188]
alisha = [51, 8, 135, 33, 157]
uids = {"[194, 238, 139, 27, 188]": 1, "[51, 8, 135, 33, 157]": 2}

# Setting up Linear Actuator
GPIO.setmode(GPIO.BOARD)
GPIO.setup(15, GPIO.OUT)
p = GPIO.PWM(15, 50)
p.start(0)

running = True
tag_received = False
first = False
match = False
start_buttons = {"Scan your card": (160, 120)}

# Function to display text on piTFT display.
def disp(my_buttons, font):
	screen.fill(BLACK)
	for my_text, text_pos in my_buttons.items():
		text_surface = font.render(my_text, True, WHITE)
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
	pygame.display.flip()  

# Function to display text on piTFT display. 
# Takes a list of tuples (not a dict) as an input
def disp_tup(blist, font): 
	screen.fill(BLACK)
	for my_text,text_pos in blist:
		text_surface = font.render(my_text, True, WHITE)
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
	pygame.display.flip() 
		
# Physical quit button.
def GPIO13_callback(channel):
    quit()
    #img = cv2.imdecode(numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8), 1)
    

# Physical "RFID tag" button
def GPIO16_callback(channel):
    global tag_recieved
    global first
    tag_received = True
    first = True
    print("callback!")
    


# Function to lock door (ie retract linear actuator).
def lock():
	print("locking")
	p.ChangeDutyCycle(5)  # retract
	time.sleep(1)
	p.ChangeDutyCycle(0)  # stop

# Function to unlock door (ie extend linear actuator).
def unlock():
	print("unlocking")
	p.ChangeDutyCycle(10)  # extend
	time.sleep(1)
	p.ChangeDutyCycle(0)  # stop


def get_img(camera): 
	stream = io.BytesIO()
	camera.resolution = (320, 240)
	camera.capture(stream, format='jpeg')
	img = cv2.imdecode(numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8), 1)
	return img
	#cv2.imwrite('result.jpg',img)
	
def face_det(img): 
	#haar_path = (cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
	cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
	gray_img =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	faces = cascade.detectMultiScale(gray_img, 1.1, 5)
	for (x,y,w,h) in faces:
		#print("found a face")
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),4)
	cv2.imwrite('result.jpg',img)
	
	if len(faces) == 1: 
		print("found a face")
		return True
		#face_recog()
	print("didn't find the face")
	return False
		
def store_hist(uid, usr_num, match):
	util.set_tag(uid)
	x = datetime.now()
	data = [x.year%2000, x.month, x.day, x.hour, x.minute, x.second, match]
	top = usr_num * 4
	util.read_out(top)
	middle = rdr.read(top)[1]
	oldest = rdr.read(top + 1)[1]
	util.rewrite(top+1, middle)
	util.rewrite(top+2, oldest)
	util.rewrite(top, data)
	util.read_out(top)

def showHist(uid, usr_num):
	hist = [(usr_num * 4), (usr_num * 4) + 1, (usr_num * 4) + 2]
	
	hist1 = rdr.read(hist[0])[1]
	date1 = str(hist1[1])+"/"+str(hist1[2])+"/"+str(hist1[0])
	time1 = str(hist1[3])+":"+str(hist1[4])+":"+str(hist1[5])
	if (hist1[6]):
		grants1 = "Granted"
	else:
		grants1 = "Denied"
	
	hist2 = rdr.read(hist[1])[1]
	date2 = str(hist2[1])+"/"+str(hist2[2])+"/"+str(hist2[0])
	time2 = str(hist2[3])+":"+str(hist2[4])+":"+str(hist2[5])
	if (hist2[6]):
		grants2 = "Granted"
	else:
		grants2 = "Denied"
	
	hist3 = rdr.read(hist[2])[1]
	date3 = str(hist3[1])+"/"+str(hist3[2])+"/"+str(hist3[0])
	time3 = str(hist3[3])+":"+str(hist3[4])+":"+str(hist3[5])
	if (hist3[6]):
		grants3 = "Granted"
	else:
		grants3 = "Denied"
	
	
	mhist = [("Date", (50, 20)), ("Time", (110, 20)), ("Access Granted", (200, 20)),
	
	(date1, (50,50)), (time1, (110,50)), (grants1, (200,50)),
	(date2, (50,80)), (time2, (110,80)), (grants2, (200,80)),
	(date3, (50,110)), (time3, (110,110)), (grants3, (200,110))]

	disp_tup(mhist, my_small_font)
	#disp(my_hist, my_small_font)
	print(hist1)
	print(hist2)
	print(hist3)
	print(date1)
	print(date2)
	print(date3)
	print(grants1)
	print(grants2)
	print(grants3)
	
	
	
def addUser():
	print("adding user")
	
def remUser():
	print("removing user")
	
GPIO.add_event_detect(13, GPIO.FALLING, callback=GPIO13_callback, bouncetime=300)
#GPIO.add_event_detect(16, GPIO.FALLING, callback=GPIO16_callback, bouncetime=300)	
	
superuser = 0
showing_hist = 0
users = os.listdir("./pictures")

# Main
while (running):
	if (not tag_received):
		disp(start_buttons, my_font)
		if not GPIO.input(16):
			tag_received = True
			first = True 
		disp(start_buttons, my_font)
		# rdr.wait_for_tag()
		# (error, tag_type) = rdr.request()
		# if not error:
		# 	(error, uid) = rdr.anticoll()
		# 	if not error:
		# 		util.auth(rdr.auth_b, [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF])

		# 		print(uid)
		# 		if (str(uid) in uids):
		# 			user = uids[str(uid)]
		# 			if (user == 1 or user == 2):
		# 				superuser = 1
		# 			print(user) 


	if (tag_received and first):
		print("we got here!")
		first = False
		camera = picamera.PiCamera()
		img = get_img(camera)
		#detected = face_det(img)

		match = fr.test_recog(img, "user2")
		print("match")
		store_hist(uid, user, match)

	if (match):
		if (superuser):
			
			camera.stop_preview()
			screen.fill(BLACK)
			
			options = {"Add User": (160, 30), "Remove User": (160, 70), "Lock": (160, 110), "Unlock": (160, 150), "History": (160, 190)}
			if ( not showing_hist):
				disp(options, my_font)
			for event in pygame.event.get(): 
		
				if (event.type is MOUSEBUTTONDOWN):
					pos = pygame.mouse.get_pos()
				elif(event.type is MOUSEBUTTONUP):
					pos = pygame.mouse.get_pos()
					x,y = pos    
					if x > 100 and x < 200:
						if y > 20 and y < 40:
							addUser()
						elif y > 60 and y < 80:
							remUser()
						elif y > 100 and y < 120:
							lock()
						elif y > 140 and y < 160:
							unlock()
						elif y > 180 and y < 200:
							showing_hist = 1
							showHist(uid, user)
		else: 
			
			camera.stop_preview()
			screen.fill(BLACK)
			options = {"Lock": (160, 60), "Unlock": (160, 120), "History": (160, 180)}
			disp(options, my_font)
			for event in pygame.event.get(): 
		
				if (event.type is MOUSEBUTTONDOWN):
					pos = pygame.mouse.get_pos()
				elif(event.type is MOUSEBUTTONUP):
					pos = pygame.mouse.get_pos()
					x,y = pos    
					if x > 100 and x < 200:
						if y < 90:
							lock()
						elif y > 100 and y < 150:
							unlock()
						elif y > 160 and y < 210:
							showHist(uid, user)
