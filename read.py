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
#GPIO.setmode(GPIO.BCM)

pygame.init()
WHITE = 255, 255, 255
BLACK = 0,0,0
RED = 255, 0, 0
GREEN = 0, 255, 0
screen = pygame.display.set_mode((320, 240))
my_font = pygame.font.Font(None, 30)
pygame.mouse.set_visible(True)

rdr = RFID(1, 0, 1000000, 31, 37, 29)
#GPIO.setup(27, GPIO.IN, pull_up_down=GPIO.PUD_UP)


anusha = [194, 238, 139, 27, 188]
alisha = [51, 8, 135, 33, 157]

running = True
tag_received = False
first = False



def setup():
	my_buttons = {"Scan your card": (160, 120)}
	#screen.fill(BLACK)
	for my_text, text_pos in my_buttons.items():
		text_surface = my_font.render(my_text, True, WHITE)
		rect = text_surface.get_rect(center=text_pos)
		screen.blit(text_surface, rect)
	pygame.display.flip()  



while (running):
	setup()
	if (not tag_received):
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
		print("tag recieved")
