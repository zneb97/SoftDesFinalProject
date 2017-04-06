import pygame, config, pyautogui, random
import config as c
from numpy import matrix
import featureExtract
import featureConvert
import prepSave

# RFCT NEEDED
class Character(pygame.sprite.Sprite):
	lives = 1
	speed = 2

	def __init__(self, name, imageName, point):
		pygame.sprite.Sprite.__init__(self)
		self.c = config.Config()
		self.name = name
		self.imageName = imageName
		self.sPosition = point
		self.reset(True)

	def reset(self,bool):
		self.getImage('down')
		self.position = self.image.get_rect()
		self.move(self.sPosition)

	def getImage(self, direction):
		imagePath = self.c.IMAGE_PATH + self.imageName + direction + ".png"
		self.image = pygame.image.load(imagePath).convert()

	def update(self):
		print("=D")

	def movement(self,key, grid,H=1):
		#	Character is located at 20, 16 in shifting matrix
		c = config.Config()
		self.map = grid

		#List of moves and validity. Note n does nothing i.e. stay in place
		moves = [pygame.K_UP,pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT, pygame.K_SPACE, pygame.K_BACKSPACE]
		valid = [True, True, True, True, True, True]


		position = (20,16)
		left = (19,16)
		right = (21,16)
		up = (20,15)
		down = (20,17)
		surroundings = []
		#Hardcoded AI
		#Character check, enemies also use this same method
		if H == 1:
			print()
			#Check to see player position is correct
			x = self.map.players[0].position[0] / self.c.TILE_SIZE
			y = self.map.players[0].position[1] / self.c.TILE_SIZE
			myMat = featureConvert.convertGrid(matrix(self.map.matrix).transpose(), (x,y) ,21,17)
			# print(myMat.item((20,16)))

			#Check optionsor (myMat.item(19,16)==9)
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

			surroundings = [myMat.item(up),myMat.item(left),myMat.item(right),myMat.item(down)]

		validMoves = []
		for i in range(len(moves)):
			if valid[i] == True:
				validMoves.append(moves[i])

		key = validMoves[int(random.randrange(len(validMoves)))]
		'''im gonna index these in order, adding bomb for option 6'''
		if key == pygame.K_UP:
			self.getImage('up')
			prepSave.saveFiles(surroundings,0)
			return [0, -1*c.TILE_SIZE]
		elif key == pygame.K_DOWN:
			self.getImage('down')
			prepSave.saveFiles(surroundings,1)
			return [0, c.TILE_SIZE]
		elif key == pygame.K_LEFT:
			self.getImage('left')
			prepSave.saveFiles(surroundings,2)
			return [-1*c.TILE_SIZE, 0]
		elif key == pygame.K_RIGHT:
			self.getImage('right')
			prepSave.saveFiles(surroundings,3)
			return [c.TILE_SIZE, 0]
		else:
			prepSave.saveFiles(surroundings,4)
			return [c.TILE_SIZE, c.TILE_SIZE]

	def move(self,point):
		self.old = self.position
		self.position = self.position.move(point)
