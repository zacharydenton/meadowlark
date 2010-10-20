# -*- coding: utf-8 -*-
import time
import string
import random

# Meadowlark Objects
import Level
import MeadowlarkConfig as config

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import pprint

def main():
	# initialize screen
	WINSIZE = [640,480]
	BGCOLOR = THECOLORS["black"]
	pygame.init()
	screen = pygame.display.set_mode(WINSIZE)
	pygame.display.set_caption('Meadowlark')
	clock = pygame.time.Clock()

	# fill background
	background = pygame.Surface(screen.get_size())
	background.fill(BGCOLOR)

	# initialize level
	level = Level.Level(background)
	
	# The Main Event Loop
	done = False
	while not done:
		clock.tick(60)
		background.fill(BGCOLOR)
		
		if level.is_finished():
			level = next_level()
		else:
			level.update()
		
		# Event handling
		events = pygame.event.get()
		level.check_keys(events)
		for e in events:
			if (e.type == QUIT):
				done = True
				break
			elif (e.type == KEYDOWN):
				if (e.key == K_ESCAPE):
					done = True
					break
					
		screen.blit(background, [0,0])
		pygame.display.flip()
	
	print "Exiting!"
	return

if __name__ == "__main__":
	main()

