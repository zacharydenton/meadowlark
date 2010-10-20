# -*- coding: utf-8 -*-
import PhoenixConfig as config
import Ammunition

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import time

class Weapon:
	def __init__(self, ship):
		self.ship = ship
		self.level = ship.level
		self.screen = ship.screen
		self.x, self.y = self.ship.rect.center

		self.delay = config.weapon_delay
		self.last_fired = 0
		self.ammo = pygame.sprite.Group()
		self.direction = self.ship.direction
	
	def move(self, x, y):
		self.x = x
		self.y = y
		
	
	def fire(self,direction, force=False):
		if not force:
			if (time.time() - self.last_fired) > self.delay:
				self.level.bullets.add(Ammunition.Ammunition(self,direction))
				self.last_fired = time.time()
		else:
			self.level.bullets.add(Ammunition.Ammunition(self,direction))
			self.last_fired = time.time()

	def update(self, entities):
		pass
	
class DoubleWeapon(Weapon):
	def fire(self):
		if (time.time() - last_fired) > self.delay:
			self.ammo.append(Ammunition.Ammunition(self.position + (1,0)))
			self.ammo.append(Ammunition.Ammunition(self.position - (1,0)))
			self.last_fired = time.time()
			
class BossWeapon(Weapon):
	def fire(self, direction):
		self.level.bullets.add(Ammunition.BossAmmo(self,-30))
		self.level.bullets.add(Ammunition.BossAmmo(self,30))
