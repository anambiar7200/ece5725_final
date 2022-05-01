# import vlc
# import time
# p = vlc.MediaPlayer("/home/ak2255/ece5725_final/mp3s/blinding_lights.mp3")
# p.play()
# p.stop()


# from playsound import playsound
# playsound("/home/ak2255/ece5725_final/mp3s/blinding_lights.mp3")


import pygame
pygame.init()
pygame.mixer.init()
my_sound = pygame.mixer.Sound('sample1.wav')
#pygame.mixer.music.load('sample1.wav')
my_sound.play()
#pygame.event.wait()

while pygame.mixer.get_busy():
    pygame.time.delay(10)
    pygame.event.poll()