import pygame
import config
import pyautogui
import random
import config as c
import numpy as np
import featureExtract
import featureConvert
import prepSave

# RFCT NEEDED


class Character(pygame.sprite.Sprite):
	lives = 1
	speed = 1

	def __init__(self, name, imageName, point):
		"""
		Intialize a character object, can be either human or monster

		name - to refer to the character
		imageName - to refer to the sprite representing character on screen
		point - location on board
		"""
		pygame.sprite.Sprite.__init__(self)
		self.c = config.Config()
		self.name = name
		self.imageName = imageName
		self.sPosition = point
		self.reset(True)

	def reset(self,bool):
		"""
		Calls to update postions graphically and in code
		"""
		self.getImage('down')
		self.position = self.image.get_rect()
		self.move(self.sPosition)

	def getImage(self, direction):
		"""
		Get correct spright image for character
		"""
		imagePath = self.c.IMAGE_PATH + self.imageName + direction + ".png"
		self.image = pygame.image.load(imagePath).convert()

	def update(self):
		print("=D")

	def movement(self,key, grid,humanAuto=1):
		"""
		Changes the sprite and issues command to movementHelper

		Note that this is used by both humans and enemies to move

		key - the keyboard command used to move the character
		grid - a grid of the board with numbers representing occupency
			of the tiles. Used to make decisions based on surroundings

		humanAuto - 0 = human controller bomberman
					1 = computer controlled bomberman
					2 = computer controlled enemy
		"""
		#	Character is located at 20, 16 in shifting matrix
		c = config.Config()
		self.map = grid

		#List of moves and validity. Note backspace is a placeholder for do nothing
		moves = [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT, pygame.K_SPACE, pygame.K_BACKSPACE]
		valid = [True, True, True, True, True, True]
		if(humanAuto == 3):
			key = moves[key-1]

		#Create shifting grid
		x = self.map.players[0].position[0] / self.c.TILE_SIZE
		y = self.map.players[0].position[1] / self.c.TILE_SIZE
		myMat = featureConvert.convertGrid(np.matrix(self.map.matrix).transpose(), (x,y) ,21,17)

		#Shifting grid keeps player at [20,16]
		#Variables to save tiles in compass directionsa around it
		position = (20,16)
		left = (19,16)
		right = (21,16)
		up = (20,15)
		down = (20,17)
		surroundings = []

		#Hardcoded AI
		#Elminates choices from an array of valid moves for the computer to
		#chose from. Add "or humanAuto = 2" to if statement to slightly improve
		#enemy AI
		if humanAuto == 1:
			#Check validity of each movement move
			#Left
			if((myMat.item(left)==1) or (myMat.item(left)==2) or (myMat.item(left)==7) or (myMat.item(left)==9)):
				valid[2] = False
			#Right
			if((myMat.item(right)==1) or (myMat.item(right)==2) or (myMat.item(right)==7) or (myMat.item(right)==9)):
				valid[3] = False
			#Up
			if((myMat.item(up)==1) or (myMat.item(up)==2) or (myMat.item(up)==7) or (myMat.item(up)==9)):
				valid[0] = False
			#Down
			if((myMat.item(down)==1) or (myMat.item(down)==2) or (myMat.item(down)==7) or (myMat.item(down)==9)):
				valid[1] = False

			#Create list of valid moves to chose from
			validMoves = []
			for i in range(len(moves)):
				if valid[i] == True:
					validMoves.append(moves[i])
			key = validMoves[int(random.randrange(len(validMoves)))]


		#Finalize choice
		#Update sprite, return tile to move to to be used by movementHelper
		#If human, compass surrounding tiles' states are saved to be used
		#in learning process
		if key == pygame.K_UP:
			self.getImage('up')
			if humanAuto == 0:
				# small_mat = featureConvert.condense_matrix(myMat)
				# small_mat = np.concatenate((small_mat,np.array([1])))
				# print(small_mat)
				# saveChoices.addRow('surroundings.csv',small_mat)
				# featureConvert.printGrid(myMat)
				# small_mat = featureConvert.condense_matrix(myMat)
				# # small_mat = np.concatenate((small_mat,np.array([1])))
				# print(small_mat)
				# prepSave.saveFiles(small_mat,1)
				self.saveChoice(1,myMat)
			return [0, -1*c.TILE_SIZE]
		elif key == pygame.K_DOWN:
			self.getImage('down')
			if humanAuto == 0:
				# small_mat = featureConvert.condense_matrix(myMat)
				# # small_mat = np.concatenate((small_mat,np.array([2])))
				# print(small_mat)
				# prepSave.saveFiles(small_mat,2)
				self.saveChoice(2,myMat)
			return [0, c.TILE_SIZE]
		elif key == pygame.K_LEFT:
			self.getImage('left')
			if humanAuto == 0:
				# small_mat = featureConvert.condense_matrix(myMat)
				# # small_mat = np.concatenate((small_mat,np.array([3])))
				# print(small_mat)
				# prepSave.saveFiles(small_mat,3)
				self.saveChoice(3,myMat)
			return [-1*c.TILE_SIZE, 0]
		elif key == pygame.K_RIGHT:
			self.getImage('right')
			if humanAuto == 0:
				# small_mat = featureConvert.condense_matrix(myMat)
				# # small_mat = np.concatenate((small_mat,np.array([4])))
				# print(small_mat)
				# prepSave.saveFiles(small_mat,4)
				self.saveChoice(4,myMat)
			return [c.TILE_SIZE, 0]
		else:
			if humanAuto == 0:
				# small_mat = featureConvert.condense_matrix(myMat)
				# # small_mat = np.concatenate((small_mat,np.array([0])))
				# print(small_mat)
				# prepSave.saveFiles(small_mat,0)
				self.saveChoice(0,myMat)
			return [0, 0]

	def move(self,point):
		"""
		Update previous and current position of character
		"""
		self.old = self.position
		self.position = self.position.move(point)

	def saveChoice(self,choice,myMat):
		# featureConvert.printGrid(myMat)
		'''This code will save the current board and choice to a csv file
		if the player is controlled by a person.
		It will always save to WallsFull.csv
		It will save to enemysFULL.csv and bombsFULL.csv if the corresponding
		object is within 10 blocks
		It will save to bricksFULL.csv if an enemy is not within 3 blocks'''
		added = [self.currentBomb,self.power,choice]
		tempGrid, info = prepSave.convertFiles(myMat,0)
		prepSave.saveFiles(tempGrid,added,0)
		if info[1]>=4:
			prepSave.saveFiles(prepSave.convertFiles(myMat,1)[0],added,1)
		if(info[0]!=10):
			prepSave.saveFiles(prepSave.convertFiles(myMat,2)[0],added,2)
		if(info[1]!=10):
			prepSave.saveFiles(prepSave.convertFiles(myMat,3)[0],added,3)
