"""
Project : Bomberman Bot with Machine Learning
Olin College Software Design Final Orject,  Spring 2017
This entire code was written by the original author, Rickyc (Github user)
No edits were done by the members of Team AFK
"""


import pygame, character, random

# RFCT NEEDED
class Enemy(character.Character):

	def __init__(self, name, imageName, point):
		"""
		Initialize enemy object.

		Note: Enemy is a subclass of character
		"""
		character.Character.__init__(self, name, "enemies/"+imageName, point)
		self.instance_of = 'enemy'

	def nextMove(self, grid):
		"""
		Randomly select movement
		"""
		self.map = grid
		ary = [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]
		#Note: the movement method called here is the same method the bomberman uses
		return self.movement(ary[int(random.randrange(0,4))], grid, 2)
