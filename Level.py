# -*- coding: utf-8 -*-
import Ship
import Enemy
import Boss
import MeadowlarkConfig as config

# PyGame Constants
import pygame
from pygame.locals import *
from pygame.color import THECOLORS

import random
class Level:
	def __init__(self, screen):
		self.screen = screen
		self.wave = 0
		
		self.ship_bounds = pygame.rect.Rect(0, self.screen.get_height() * 0.65, self.screen.get_width(), self.screen.get_height() * 0.35)
		self.enemy_bounds = pygame.rect.Rect(0, 0, self.screen.get_width(), self.screen.get_height() * 0.6)
		self.boss_bounds = pygame.rect.Rect(0, 0, self.screen.get_width(), self.screen.get_height() * 0.4)
		
		# initialize game objects
		self.ship = Ship.Ship(self)
		self.enemies = self.enemy_grid(config.max_num_enemies)
		
		self.entities = pygame.sprite.Group()
		self.bullets = pygame.sprite.Group()
		self.powerups = pygame.sprite.Group()
		self.entities.add(self.ship)
		for enemy in self.enemies:
			self.entities.add(enemy)	

	def is_finished(self):
		return len(self.entities) == 1
		
	def update(self):
		if len(self.entities) == 1:
			self.wave += 1
			if self.wave > 2:
				pass
			elif self.wave == 2:
				self.entities.add(Boss.Boss(self, [self.screen.get_width() / 2, 100]))
			else:
				self.entities.add(self.enemy_grid(config.max_num_enemies))
		#blit everything to the screen
		for entity in self.entities:
			entity.update(self.entities)
			self.bullets.add(entity.weapon.ammo)
			self.screen.blit(entity.image, entity.rect)
		
		for bullet in self.bullets:
			bullet.update(self.entities)
			bullet.draw()
		
		for powerup in self.powerups:
			powerup.update(self.entities)
			powerup.draw()

	def check_keys(self, events):
		self.ship.check_keys(events)
		
	def enemy_grid(self, num_enemies):
		enemies = []
		rows = 5
		cols = num_enemies / rows
		row_sep = self.enemy_bounds.height / (rows + 1)
		col_sep = self.enemy_bounds.width / (cols + 1)
		for row in range(rows):
			for col in range(cols):
				enemies.append(Enemy.Enemy(self, ((1+col) * col_sep, (1+row) * row_sep)))
		return enemies
