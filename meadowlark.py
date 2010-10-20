# -*- coding: utf-8 -*-
import time
import string
import random

# Phoenix Objects
import Game

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
	pygame.display.set_caption('Phoenix')
	clock = pygame.time.Clock()

	# fill background
	background = pygame.Surface(screen.get_size())
	background.fill(BGCOLOR)

	# initialize game
	levels = "assets/levels.xml"
	game = Game.Game(background, levels)
	
	# The Main Event Loop
	done = False
	while not done:
		clock.tick(60)
		background.fill(BGCOLOR)

		game.update()
		
		# Event handling
		events = pygame.event.get()
		done = game.check_keys(events)
				
		screen.blit(background, [0,0])
		pygame.display.flip()
	
	print "Exiting!"
	return

if __name__ == "__main__":
	main()

