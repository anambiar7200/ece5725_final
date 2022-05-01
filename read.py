import sys
sys.path.append("/usr/lib/python3/dist-packages")
from picamera import PiCamera
import time
import RPi.GPIO as GPIO
from pirc522 import RFID
import pygame
from pygame.locals import * 
import os
import subprocess

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
pygame.mouse.set_visible(True)

rdr = RFID(1, 0, 1000000, 31, 37, 29)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)


anusha = [194, 238, 139, 27, 188]
alisha = [51, 8, 135, 33, 157]

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
def disp(my_buttons):
	screen.fill(BLACK)
	for my_text, text_pos in my_buttons.items():
		text_surface = my_font.render(my_text, True, WHITE)
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
	pygame.display.flip()  

# Physical quit button.
def GPIO13_callback(channel):
    quit()
    
GPIO.add_event_detect(13, GPIO.FALLING, callback=GPIO13_callback, bouncetime=300)

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

# Main
while (running):
	if (not tag_received):
		disp(start_buttons)
		print("waiting for tag")
		rdr.wait_for_tag()
		(error, tag_type) = rdr.request()
		if not error:
			print("tag received")
			(error, uid) = rdr.anticoll()
			print(uid)
			if (uid == anusha):
				print("Anusha") 
			elif (uid == alisha):
				print("Alisha") 
			tag_received = True
			first = True 
		

	if (tag_received and first):
		first = False
		camera = PiCamera()
		camera.start_preview()
		time.sleep(2)
		camera.capture("test.jpg")
		match = True
	if (match):
		camera.stop_preview()
		screen.fill(BLACK)
		options = {"Lock": (160, 60), "Unlock": (160, 120)}
		disp(options)
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
