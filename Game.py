# -*- coding: utf-8 -*-
# Meadowlark Objects
import Level
import MeadowlarkConfig as config

class Game:
	def __init__(self, background, levels):
		self.background = background
		self.levels = self.get_levels()
		self.level = self.get_level(1)
		
	def get_levels(self):
		#TODO parse xml file describing levels
		pass

	def get_level(self, level):
		level = Level.Level(self.background)
		return level

	def update(self):
		if level.is_finished():
			level = self.next_level()
		else:
			level.update()
		pass

	def check_keys(self, events):
		'''
		returns True if the user wants to quit
		'''
		self.level.check_keys(events)
		for e in events:
			if (e.type == QUIT):
				return True
			elif (e.type == KEYDOWN):
				if (e.key == K_ESCAPE):
					return True
		return False
	
