# -*- coding: utf-8 -*-
import MeadowlarkConfig as config
import Ship
import Weapon
import Powerup
import Spritesheet

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import math
import random
import os

class Boss(pygame.sprite.Sprite):
	spritesheet = None
	
	def __init__(self, level, position):
		pygame.sprite.Sprite.__init__(self)
		
		self.level				= level
		self.screen				= self.level.screen
		self.goal					= position
		self.x						= position[0]
		self.y						= position[1] - self.level.boss_bounds.height
		
		self.health		= config.boss_base_health
		self.speed		= config.boss_base_speed
		self.skill		=	config.boss_base_skill
		self.counter	= 0
		self.alive		= True
		self.direction= [0,1]
		self.ready		= False		
		
		if Boss.spritesheet is None:
			Boss.spritesheet = Spritesheet.Spritesheet(os.path.join('shooter','disasteroids2_boss.bmp'))
		self.spritesheet	= Boss.spritesheet
		self.image				= self.get_image(self.spritesheet, self.direction)
		self.rect					= self.image.get_rect()
		self.rect.center	= [self.x, self.y]
		
		self.weapon		= Weapon.BossWeapon(self)
		
		self.move_to(position)

	def move(self, direction):
		self.x += (self.speed * direction[0])
		self.y += (self.speed * direction[1])
		self.rect.center = [self.x, self.y]
		self.weapon.move(self.x, self.y)

	def move_auto(self):
		radius = 0.5
		dx = radius * math.cos(math.radians(self.counter))
		dy = radius * math.sin(math.radians(self.counter))
		self.x += dx
		self.y += dy
		self.rect.center = [self.x, self.y]
		self.weapon.move(self.x, self.y)
		self.counter += 1
		if self.counter > 360:
			self.counter = 0
		
	def move_to(self,position):
		angle = math.atan2(-(self.y-position[1]), (self.x-position[0]))
		direction =  (math.cos(angle), math.sin(angle))
		self.move(direction)
		
		if position[0] == self.x and position[1] == self.y:
			self.ready = True

	def fire(self):
		self.weapon.fire(self.direction)

	def damage(self, amount):
		self.health -= amount
		
	def die(self):
		if random.random() <= (config.powerup_chance / 100.0):
			self.level.powerups.add(Powerup.Powerup(self, [0,1]))
		self.kill()

	def update(self, entities):
		if self.alive:
			if self.health <= 0:
				self.die()
			if random.random() <= (self.skill/100.0):
				self.fire()
			if not self.ready:
				self.move_to(self.goal)
			else:
				self.move_auto()
			self.weapon.update(entities)

	def draw(self):
		self.screen.blit(self.image, self.rect)
		
	def get_image(self,spritesheet,direction):
		return spritesheet.imgat(pygame.rect.Rect(270,128,107,86),-1)
		