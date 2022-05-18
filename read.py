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
import requests
import take_photos
import shutil
import pickle

os.putenv("SDL_VIDEODRIVER","fbcon")
os.putenv("SDL_FBDEV", "/dev/fb1")
os.putenv("SDL_MOUSEDRV", "TSLIB")
os.putenv("SDL_MOUSEDEV", "/dev/input/touchscreen")

pygame.init()
WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255, 0, 0
GREEN = 0, 255, 0
screen = pygame.display.set_mode((320, 240))
my_font = pygame.font.Font(None, 30)
my_small_font = pygame.font.Font(None, 20)
pygame.mouse.set_visible(False)

rdr = RFID(1, 0, 1000000, 31, 37, 29)
util = rdr.util()
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)


anusha = [194, 238, 139, 27, 188]
alisha = [51, 8, 135, 33, 157]
uids = {"[194, 238, 139, 27, 188]": 1, "[51, 8, 135, 33, 157]": 2}

# Setting up Linear Actuator
GPIO.setmode(GPIO.BOARD)
GPIO.setup(36, GPIO.OUT)
p = GPIO.PWM(36, 50)
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

    

# Physical "RFID tag" button
def GPIO16_callback(channel):
    global tag_recieved
    global first
    tag_received = True
    first = True

# Function to lock door (ie retract linear actuator).
def lock():
	p.ChangeDutyCycle(5)  # retract
	time.sleep(1)
	p.ChangeDutyCycle(0)  # stop

# Function to unlock door (ie extend linear actuator).
def unlock():
	p.ChangeDutyCycle(10)  # extend
	time.sleep(1)
	p.ChangeDutyCycle(0)  # stop

# Function to store the user login history		
def storeHist(user, match):
	x = datetime.now()
	data = [x.year%2000, x.month, x.day, x.hour, x.minute, x.second, match]
	try: 
		history = pickle.load(open("histories", "rb"))
	except FileNotFoundError:
		history = {}
	if user not in history: 
		history[user] = []
	if len(history[user]) > 2:
		history[user] = history[user][:-1]
	history[user] = [data] + history[user]
	with open("histories", "wb") as hh: 
		pickle.dump(history, hh)

# Function to display the user history on screen
def showHist(user):
	history = pickle.load(open("histories", "rb"))
	mhist = [("Date", (50, 20)), ("Time", (110, 20)), ("Access Granted", (200, 20)), ("Back", (280, 220))]
	ypos = 50
	for hitem in history[user]:
		date = str(hitem[1])+"/"+str(hitem[2])+"/"+str(hitem[0])
		time = str(hitem[3])+":"+str(hitem[4])+":"+str(hitem[5])
		if (hitem[6]):
			grant = "Granted"
		else:
			grant = "Denied"
		mhist.append((date, (50,ypos)))
		mhist.append((time, (110,ypos)))
		mhist.append((grant, (200,ypos)))
		ypos += 30

	disp_tup(mhist, my_small_font)
	
# RFID function to store history
def RFID_store_hist(uid, usr_num, match):
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

# RFID function to show history
def RFID_showHist():
#	hist = [(usr_num * 4), (usr_num * 4) + 1, (usr_num * 4) + 2]
	
#	hist1 = rdr.read(hist[0])[1]
#	date1 = str(hist1[1])+"/"+str(hist1[2])+"/"+str(hist1[0])
#	time1 = str(hist1[3])+":"+str(hist1[4])+":"+str(hist1[5])
#	if (hist1[6]):
#		grants1 = "Granted"
#	else:
#		grants1 = "Denied"
	
#	hist2 = rdr.read(hist[1])[1]
#	date2 = str(hist2[1])+"/"+str(hist2[2])+"/"+str(hist2[0])
#	time2 = str(hist2[3])+":"+str(hist2[4])+":"+str(hist2[5])
#	if (hist2[6]):
#		grants2 = "Granted"
#	else:
#		grants2 = "Denied"
#	
#	hist3 = rdr.read(hist[2])[1]
#	date3 = str(hist3[1])+"/"+str(hist3[2])+"/"+str(hist3[0])
#	time3 = str(hist3[3])+":"+str(hist3[4])+":"+str(hist3[5])
#	if (hist3[6]):
#		grants3 = "Granted"
#	else:
#		grants3 = "Denied"
	
	
#	mhist = [("Date", (50, 20)), ("Time", (110, 20)), ("Access Granted", (200, 20)),
#	
#	(date1, (50,50)), (time1, (110,50)), (grants1, (200,50)),
#	(date2, (50,80)), (time2, (110,80)), (grants2, (200,80)),
#	(date3, (50,110)), (time3, (110,110)), (grants3, (200,110))
#	("Back", (280, 220))]

	mhist = [("Date", (50, 20)), ("Time", (110, 20)), ("Access Granted", (200, 20)),("Back", (280, 220))]

	disp_tup(mhist, my_small_font)

	
# Function to add a user	
def addUser():
	add_initial_buttons = {"Scan your card": (160, 120)}
	disp(add_initial_buttons, my_font)
	pressed = False
	while(not pressed):
		# add the rfid tag to list of users
		# take 20 pictures of them
		if not GPIO.input(11):
			user = 1
			pressed = True
		elif not GPIO.input(15):
			user = 2
			pressed = True
		elif not GPIO.input(16):
			user = 3
			pressed = True
	
	add_picture_buttons = {"Please stand in front of camera": (160, 120)}
	disp(add_picture_buttons, my_font)
	time.sleep(3)
	
	add_picture_buttons = {"3": (160, 120)}
	disp(add_picture_buttons, my_font)
	time.sleep(1)
	add_picture_buttons = {"3 2": (160, 120)}
	disp(add_picture_buttons, my_font)
	time.sleep(1)
	add_picture_buttons = {"3 2 1": (160, 120)}
	disp(add_picture_buttons, my_font)
	time.sleep(1)
	
	take_photos.take_pics(user)
	add_picture_buttons = {"Please stand by": (160, 120)}
	disp(add_picture_buttons, my_font)
	try: 
		fr.get_encodings("user"+str(user))
		global users
		users = os.listdir("./pictures")
		success = "User "+str(user) + " successfully added"
		add_picture_buttons = {success: (160, 120), "Back": (280, 220)}
		disp(add_picture_buttons, my_font)
	except IndexError:
		fail = "Unable to add user."
		add_fail = {fail: (160, 120), "Back": (280, 220)}
		disp(add_fail, my_font)
		

# Function to remove a user	
def remUser():
	removing_initial_buttons = {"Please select the user to remove": (160, 120)}
	disp(removing_initial_buttons, my_font)
	pressed = False
	while(not pressed):
		if not GPIO.input(11):

			user = 1
			pressed = True
		elif not GPIO.input(15):
			user = 2
			pressed = True
		elif not GPIO.input(16):
			user = 3
			pressed = True
	global users
	
	rem_picture_buttons = {"Please stand by": (160, 120)}
	disp(rem_picture_buttons, my_font)

	try:
		shutil.rmtree("./pictures/user"+ str(user))
		os.remove("encodings")
		os.remove("names")
		users = os.listdir("./pictures")
		for usr in users:
			fr.get_encodings(usr)
		success = "User "+str(user) + " successfully removed"
		removing_initial_buttons = {success: (160, 120), "Back": (280, 220)}
		disp(removing_initial_buttons, my_font)
	except:
		fail = "User "+str(user) + " does not exist"
		removing_initial_buttons = {fail: (160, 120), "Back": (280, 220)}
		disp(removing_initial_buttons, my_font)
		

GPIO.add_event_detect(13, GPIO.FALLING, callback=GPIO13_callback, bouncetime=300)	
	
superusers = [1, 2]
showing_hist = 0
adding_user = 0
removing_user = 0
global users 
searching = False
users = os.listdir("./pictures")

# Main
while (running):
	if (not tag_received):
		if not GPIO.input(11):
			first = True 
			user = 1
			searching = True


			if "user"+str(user) in users:
				tag_received = True
			else:
				fail = "User "+str(user) + " doesn't exist"
				fail_buttons = {fail: (160, 120)}
				disp(fail_buttons, my_font)
				time.sleep(2)
		elif not GPIO.input(15):
			first = True 
			user = 2
			searching = True
			if "user"+str(user) in users:
				tag_received = True
			else:
				fail = "User "+str(user) + " doesn't exist"
				fail_buttons = {fail: (160, 120)}
				disp(fail_buttons, my_font)
				time.sleep(2)
		elif not GPIO.input(16):
			first = True 
			user = 3
			if "user"+str(user) in users:
				tag_received = True
			else:
				fail = "User "+str(user) + " doesn't exist"
				fail_buttons = {fail: (160, 120)}
				disp(fail_buttons, my_font)
				time.sleep(2)
		
		
		disp(start_buttons, my_font)
		

	if (tag_received and first):
		my_buttons = {"Verifying User "+str(user):(160, 120)}
		disp(my_buttons, my_font)
		first = False
		camera = picamera.PiCamera()
		img = camera.capture("compare.jpg")
		name = "user" + str(user)
		match = fr.test_recog("compare.jpg", name)
		camera.close()
		storeHist(user, match)

	if (match):
		if (user in superusers):
			screen.fill(BLACK)
			
			options = {"Add User": (160, 30), "Remove User": (160, 70), "Lock": (160, 110), "Unlock": (160, 150), "History": (160, 190), "EXIT": (280, 220)}
			if ( not showing_hist and not adding_user and not removing_user):
				disp(options, my_font)
				for event in pygame.event.get(): 
			
					if (event.type is MOUSEBUTTONDOWN):
						pos = pygame.mouse.get_pos()
					elif(event.type is MOUSEBUTTONUP):
						pos = pygame.mouse.get_pos()
						x,y = pos    
						if x > 100 and x < 200:
							if y > 20 and y < 40:
								adding_user = 1
								addUser()
							elif y > 60 and y < 80:
								removing_user = 1
								remUser()
							elif y > 100 and y < 120:
								lock()
							elif y > 140 and y < 160:
								unlock()
							elif y > 180 and y < 200:
								showing_hist = 1
								showHist(user)
						elif x > 250:
							if y > 200 and y < 240:
								tag_received = 0
								match = False
			elif showing_hist: 
				for event in pygame.event.get(): 
					if (event.type is MOUSEBUTTONDOWN):
						pos = pygame.mouse.get_pos()
					elif(event.type is MOUSEBUTTONUP):
						pos = pygame.mouse.get_pos()
						x,y = pos    
						if x > 250: 
							if y > 200: 
								showing_hist = False
			elif adding_user:
				for event in pygame.event.get(): 
					if (event.type is MOUSEBUTTONDOWN):
						pos = pygame.mouse.get_pos()
					elif(event.type is MOUSEBUTTONUP):
						pos = pygame.mouse.get_pos()
						x,y = pos    
						if x > 250: 
							if y > 200: 
								adding_user = False
			elif removing_user:
				for event in pygame.event.get(): 
					if (event.type is MOUSEBUTTONDOWN):
						pos = pygame.mouse.get_pos()
					elif(event.type is MOUSEBUTTONUP):
						pos = pygame.mouse.get_pos()
						x,y = pos    
						if x > 250: 
							if y > 200: 
								removing_user = False
		else: 
			screen.fill(BLACK)
			options = {"Lock": (160, 60), "Unlock": (160, 120), "History": (160, 180), "EXIT": (280, 220)}
			if ( not showing_hist ):
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
								showHist(user)
								showing_hist = True
						elif x > 250:
							if y > 200 and y < 240:
								tag_received = 0
								match = False
			elif showing_hist: 
				for event in pygame.event.get(): 
					if (event.type is MOUSEBUTTONDOWN):
						pos = pygame.mouse.get_pos()
					elif(event.type is MOUSEBUTTONUP):
						pos = pygame.mouse.get_pos()
						x,y = pos    
						if x > 250: 
							if y > 200: 
								showing_hist = False
	elif tag_received and (not match): 
		#requests.post("https://maker.ifttt.com/trigger/nonuser_detected/with/key/bZN58Z9OZzwAcmjGQ20Y5C?value1=user1")
		message = {"Access denied." : (160, 120)}
		disp(message, my_font)
		time.sleep(2)
		tag_received = 0
		match = False
