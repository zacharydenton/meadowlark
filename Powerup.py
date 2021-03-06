# -*- coding: utf-8 -*-
import MeadowlarkConfig as config
import Ship
import Spritesheet

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import os

class Powerup(pygame.sprite.Sprite):
	spritesheet = None
	
	def __init__(self, parent, direction):
		pygame.sprite.Sprite.__init__(self)
		self.screen				= parent.screen
		self.x						= parent.x 
		self.y						= parent.y 

		self.alive			= True
		self.value			= config.powerup_base_value
		self.direction	= direction
		self.speed			= config.powerup_base_speed
		
		if Powerup.spritesheet is None:
			Powerup.spritesheet = Spritesheet.Spritesheet(os.path.join('shooter','disasteroids2_master.bmp'))
		self.spritesheet	= Powerup.spritesheet
		self.image				= self.get_image(self.spritesheet)
		self.rect					= self.image.get_rect()
		self.rect.center	= [self.x, self.y]
		
	def powerup(self, entity):
		entity.cash += self.value
		print entity, "has", entity.cash, "cash"
	
	def move(self, speed, direction):
		self.x += (speed * direction[0])
		self.y += (speed * direction[1])
		self.rect.center = [self.x, self.y]
		if self.x < 0 or self.x > self.screen.get_width():
			self.die()
		elif self.y < 0 or self.y > self.screen.get_height():
			self.die()

	def check_collision(self, entities):
		collision = False
		for entity in pygame.sprite.spritecollide(self, entities, False):
			if isinstance(entity, Ship.Ship):
				self.powerup(entity)
				self.die()

	def die(self):
		self.alive = False
		self.kill()

	def update(self, entities):
		self.move(self.speed, self.direction)
		self.check_collision(entities)
		self.draw()
	
	def draw(self):
		self.screen.blit(self.image, self.rect)
		
	def get_image(self, spritesheet):
		return spritesheet.imgat(pygame.rect.Rect(170,239,29,17), -1)
		
class Health(Powerup):
	def __init__(self):
		self.price = 250
		self.health = 10
	
	def powerup(self, entity):
		entity.health += self.health
