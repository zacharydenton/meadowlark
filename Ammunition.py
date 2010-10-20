# -*- coding: utf-8 -*-
import PhoenixConfig as config
import Spritesheet
import Ship

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import pprint
import os
import math

class Ammunition(pygame.sprite.Sprite):
	spritesheet = None
	
	def __init__(self, weapon, direction):
		pygame.sprite.Sprite.__init__(self)
		self.weapon 			= weapon
		self.screen				= weapon.screen
		self.x						= weapon.x 
		self.y						= weapon.y 

		self.alive			= True
		self.damage			= config.ammo_base_damage
		self.direction	= direction
		self.speed			= config.ammo_base_speed
		
		if Ammunition.spritesheet is None:
			Ammunition.spritesheet = Spritesheet.Spritesheet(os.path.join('shooter','disasteroids2_master.bmp'))
		self.spritesheet	= Ammunition.spritesheet
		self.image				= self.get_image(self.spritesheet, self.direction)
		self.rect					= self.image.get_rect()
		self.rect.center	= [self.x, self.y]
	
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
			if not isinstance(entity, type(self.weapon.ship)):
				entity.damage(self.damage)
				collision = True
		if collision:
			self.die()

	def die(self):
		self.alive = False
		self.kill()

	def update(self, entities):
		self.move(self.speed, self.direction)
		self.check_collision(entities)
	
	def draw(self):
		self.screen.blit(self.image, self.rect)
		
	def get_image(self, spritesheet, direction):
		if direction == [0,-1]:
			return spritesheet.imgat(pygame.rect.Rect(49,58,11,21),-1)
		elif direction == [0,1]:
			return spritesheet.imgat(pygame.rect.Rect(49,82,11,25), -1)
		
	
class UpgradeAmmunition(Ammunition):
	def __init__(self, position):
		self.alive			= True
		self.damage			= 2 * config.ammo_base_damage
		self.direction	= (0,1)
		self.speed			= config.ammo_base_speed
		self.position		= position
		
		
class BossAmmo(Ammunition):
	def __init__(self,weapon,offset):
		pygame.sprite.Sprite.__init__(self)
		self.offset				= offset
		self.weapon 			= weapon
		self.screen				= weapon.screen
		self.x						= self.weapon.x + offset
		self.y						= self.weapon.y

		self.alive			= True
		self.damage			= 20
		self.direction	= [0,0]
		self.speed			= config.ammo_base_speed*2
		
		if Ammunition.spritesheet is None:
			Ammunition.spritesheet = Spritesheet.Spritesheet(os.path.join('shooter','disasteroids2_master.bmp'))
		self.spritesheet	= Ammunition.spritesheet
		self.image				= self.get_image(self.spritesheet, self.direction)
		self.rect					= self.image.get_rect()
		self.rect.center	= [self.x, self.y]
		
	def update(self, entities):
		if self.direction == [0,0]:
			self.direction = self.get_direction(entities)
		self.move(self.speed, self.direction)
		self.check_collision(entities)
		
	def get_direction(self,entities):
		ship = None
		for entity in entities:
			if isinstance(entity, Ship.Ship):
				ship = entity
		if ship != None:
			position = [ship.rect.center[0],ship.rect.center[1]]
			position[0] += self.offset
			angle = math.atan2(-(self.y-position[1]), -(self.x-position[0]))
			direction =  (math.cos(angle), math.sin(angle))
			
		self.direction = direction
		return direction
	
	def get_image(self, spritesheet, direction):
		return spritesheet.imgat(pygame.rect.Rect(482,29,34,33), -1)
