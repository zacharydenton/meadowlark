# -*- coding: utf-8 -*-
import MeadowlarkConfig as config
import Weapon
import Spritesheet

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import os

class Ship(pygame.sprite.Sprite):
	def __init__(self, level):
		pygame.sprite.Sprite.__init__(self)
		self.level				= level
		self.screen 			= self.level.screen
		screensize 				= self.screen.get_size()
		self.screenwidth	= screensize[0]
		self.screenheight	= screensize[1]
		self.x						= (self.screenwidth / 2)
		self.y						= (0.4 * self.screenheight) * 2
		
		self.health 			= config.ship_base_health
		self.speed 				= config.ship_base_speed
		self.alive				= True
		self.direction		= [0,0]
		self.moving				= False
		self.firing				= False
		self.cash					= 0
		
		self.left					= False
		self.right				= False
		self.up						= False
		self.down					= False
		
		self.size					= [100, 100]
		self.spritesheet	= Spritesheet.Spritesheet(os.path.join('shooter','disasteroids2_master.bmp'))
		self.image				= self.get_image(self.spritesheet, self.direction, self.moving)
		self.rect					= self.image.get_rect()
		self.rect.center	= [self.x, self.y]
		
		self.weapon				= Weapon.Weapon(self)

	def move(self, direction):
		self.moving = True
		if self.level.ship_bounds.left + (self.rect.width / 2) < self.x + (self.speed * direction[0]) < self.level.ship_bounds.right - (self.rect.width / 2):
			self.x += (self.speed * direction[0])
		if self.level.ship_bounds.top + (self.rect.height / 2) < self.y + (self.speed * direction[1]) < self.level.ship_bounds.bottom - (self.rect.height / 2):
			self.y += (self.speed * direction[1])
		self.direction = [direction[0], direction[1]]
		self.image = self.get_image(self.spritesheet, self.direction, self.moving)

		self.rect.center = [self.x, self.y]
		self.weapon.x, self.weapon.y = [self.x, self.y]
		
	def stop_moving(self):
		self.moving = False
		self.image = self.get_image(self.spritesheet, [0,-1], self.moving)

	def fire(self, force=False):
		self.firing = True
		self.weapon.fire([0, -1], force)
	
	def stop_firing(self):
		self.firing = False

	def damage(self, amount):
		self.health -= amount
		print "ship has", self.health, "health points remaining..."

	def die(self):
		print "you have perished."
		self.alive = False
		self.kill()

	def update(self, entities):
		if self.alive:
			if self.health <= 0:
				self.die()
			self.weapon.update(entities)
			
	def check_keys(self, events):
		# Event handling
		if self.alive:
			for e in events:
				if (e.type == KEYDOWN):
					if (e.key == K_SPACE):
						self.fire(force=True)
					if (e.key == K_LEFT):
						self.left = True
						self.direction[0] = -1
					if (e.key == K_RIGHT):
						self.right = True
						self.direction[0] = 1
					if (e.key == K_UP):
						self.up = True
						self.direction[1] = -1
					if (e.key == K_DOWN):
						self.down = True
						self.direction[1] = 1
				elif (e.type == KEYUP):
					if (e.key == K_SPACE):
						self.stop_firing()
					if (e.key != K_SPACE):
						#left
						if e.key == K_LEFT:
							self.left = False
							if self.direction[0] == -1 and self.right:
								self.direction[0] = 1
							elif self.direction[0] == -1:
								self.direction[0] = 0
						#right
						if (e.key == K_RIGHT):
							self.right = False
							if self.direction[0] == 1 and self.left:
								self.direction[0] = -1
							elif self.direction[0] == 1:
								self.direction[0] = 0
						#up
						if e.key == K_UP:
							self.up = False
							if self.direction[1] == -1 and self.down:
								self.direction[1] = 1
							elif self.direction[1] == -1:
								self.direction[1] = 0
						#down
						if e.key == K_DOWN:
							self.down = False
							if self.direction[1] == 1 and self.up:
								self.direction[1] = -1
							elif self.direction[1] == 1:
								self.direction[1] = 0
							
			if self.firing:
				self.fire()
			
			if self.direction != [0,0]:
				self.move(self.direction)
			else:
				self.stop_moving()
				
	def draw(self):
		self.screen.blit(self.image, self.rect)
		
	def get_image(self,spritesheet,direction,moving):
#		if direction[0] == 1: #right
#			return spritesheet.imgat(pygame.rect.Rect(390,298,46,43), -1)
#		elif direction[0] == -1: #left
#			return spritesheet.imgat(pygame.rect.Rect(518,297,45,46), -1)
#		else: # straight
#			return spritesheet.imgat(pygame.rect.Rect(446,309,63,31), -1)
		if direction[0] == 1: #right
			coords = [46,359,29,28]
		elif direction[0] == -1: #left
			coords = [451,359,29,28]
		else: #straight
			coords = [481,359,29,28]
		if not moving:
			coords[1] += 45
		return spritesheet.imgat(pygame.rect.Rect(coords), -1)
		
		

