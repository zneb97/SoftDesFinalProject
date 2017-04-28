import sys, pygame, config, random, time
import player, enemy, board, bomb, highscore, music
import featureExtract, featureConvert, prepSave
import numpy as np
from pygame.locals import *
import os,sys
sys.path.append(os.path.split(sys.path[0])[0])
from Net import *
import NNClass
# num2Key = {1:pygame.K_UP, 2:pygame.K_DOWN,3: pygame.K_LEFT,4: pygame.K_RIGHT}

class Game:
	"""
	Store, update, and maintain all data important to running game
	"""
	#Stored board data
	players = []
	enemies = []
	bombs = []
	resetTiles = []

	stage = 1
	level = 3

	firstRun = True
	exitGame = False

	# Multiplayer data
	tcpData = []
	sendingData = []
	lastTcpCall = 0
	pHash = {}

	def __init__(self, mode):
		"""
		Initialize new game
		"""
		self.c = config.Config()
		self.highscores = highscore.Highscore()
		self.forceQuit = False
		self.mode = mode

		pygame.init()
		self.screen = pygame.display.set_mode((self.c.WIDTH,self.c.HEIGHT),pygame.DOUBLEBUF)
		pygame.display.set_caption("Bomberman")

		# init preloader / join server
		if self.mode == self.c.MULTI:
			preloader = pygame.image.load(self.c.IMAGE_PATH + "loading.png").convert()
			self.blit(preloader,(0,0))
			pygame.display.flip()
			self.joinGame()

		# repeat for multiple levels
		while not self.exitGame:
			self.resetGame()
			self.clearBackground()
			self.initGame()

		# launch highscores
		if not self.forceQuit:
			self.highscores.reloadScoreData()
			self.highscores.displayScore()

	def joinGame(self):
		"""
		Identify game to connect to
		"""
		self.client = TCPClient()

		# choose server connection
		if self.c.LOCALHOST:
			self.client.connect("localhost",6317)
		else:
			# server_name = sys.argv[1]
			# server_address = (server_name, 6317)
			# print >>sys.stderr, 'starting up on %s port %s' % server_address
			self.client.connect('gsteelman-Latitude-E5470', 6317)

		self.id = random.randint(0,1000000)		# unique player id
		self.client.send_data(["update","user joined",str(self.id)])

		while True:
			self.tcpData = self.client.wait_for_data()
			self.client.send_data(["update",None])
			print(self.tcpData)
			if len(self.tcpData) > 0 and self.tcpData[-1] == "[SERVER]|START":
				break
			self.initMultiUsers()

	def getMultiStartPosition(self,id):
		if id == "1":
			return (40,40)
		elif id == "2":
			return (760,40)
		elif id == "3":
			return (40,600)
		elif id == "4":
			return (760,600)

	def initMultiSelf(self,data):
		d = data[-1].split("|")
		self.user = player.Player("Player " + ary[0] ,"p_"+ary[0]+"_" , ary[2], self.getMultiStartPosition(ary[0]))
		self.players.append(self.user)

	def initMultiUsers(self):

		for element in self.tcpData:
			ary = element.split("|")
			if int(ary[0]) > int(self.lastTcpCall):
				# manipulate
				if ary[1] == 'JOIN':
					p = player.Player("Player "+ary[0] ,"p_"+ary[0]+"_" , ary[2], self.getMultiStartPosition(ary[0]))
					self.pHash[ary[2]] = p
					self.players.append(p)
					self.lastTcpCall = ary[0]

	def tcpUpdate(self):
		data = self.client.check_for_data()
		if data:
			self.tcpData = data
	#		print '-------------'
	#		print self.tcpData
			if self.sendingData == []:
				self.sendingData = ["update",None]
			self.client.send_data(self.sendingData)
			self.sendingData = []

	# RFCT
	# ary[3] = key 			ary[2] = user
	def manipulateTcpData(self):
		grid = featureExtract.grid(self)
		for d in self.tcpData:
			ary = d.split("|")
			try:
				print(ary[0] + " " + str(self.lastTcpCall))
				if int(ary[0]) > int(self.lastTcpCall):
					if str(ary[2]) != str(self.id):
						if ary[1] == "MOVE":
							point = self.pHash[ary[2]].movement(int(ary[3]),grid,2)
							self.movementHelper(self.pHash[ary[2]],point)
						elif ary[1] == "BOMB":
							self.deployBomb(self.pHash[ary[2]])
					self.lastTcpCall = ary[0]
			except ValueError:
				print('skip')

	def resetGame(self):
		"""
		Clear board data

		Called on death or level clear
		"""
		self.field = None
		self.enemies = []
		self.bombs = []
		self.resetTiles = []


	def clearBackground(self):
		bg = pygame.Surface(self.screen.get_size())
		bg = bg.convert()
		bg.fill((0,0,0))
		self.blit(bg,(0,0))

	def initGame(self):
		"""
		Begin game mode with correct stats for board
		"""
		if self.mode == self.c.SINGLE:
			self.printText("Level %d-%d" % (self.stage,self.level),(40,15))
			self.field = board.Board(self.stage, self.level)
			self.timer = 3*60+1
		elif self.mode == self.c.MULTI:
			self.printText("Multiplayer",(40,15))
			self.field = board.Board(0,0)
			self.timer = 5*60+1

		self.drawBoard()
		self.drawInterface()
		self.updateTimer()
		self.move_dict = {0:pygame.K_BACKSPACE,
					1:pygame.K_UP,
					2:pygame.K_DOWN,
					3:pygame.K_LEFT,
					4:pygame.K_RIGHT,
					5:pygame.K_SPACE}

		# Players do not have to be reinitialized in single player after the first time
		if self.firstRun:
			self.firstRun = False
			self.initPlayers()
		else:
			self.resetPlayerPosition(self.user,False)

		# No enemies in multiplayer
		if self.mode == self.c.SINGLE:
			self.initEnemies(self.level*2 + 1)

		# Music player
		mp = music.Music()
		mp.playMusic(self.mode)

		self.runGame()

	# draws the board onto the screen
	def drawBoard(self):
		"""
		Build board

		Note: each level has a predefined layout
		"""
		for row in range(1,len(self.field.board)-1):
			for col in range(1,len(self.field.board[row])-1):
				image = self.field.board[row][col].image
				position = self.field.board[row][col].image.get_rect().move((col*self.c.TILE_SIZE,row*self.c.TILE_SIZE))
				self.blit(image, position)

	def updateDisplayInfo(self):
		"""
		Display charater stats
		"""
		self.printText(self.user.score,(65,653))
		self.printText(self.user.lives,(775,653))
		self.printText(self.user.maxBombs,(630,653))
		self.printText(self.user.power,(700,653))

	def drawInterface(self):
		"""
		Build border stats graphics
		"""
		player  = pygame.image.load(self.c.IMAGE_PATH + "screen/player.png").convert()
		life = pygame.image.load(self.c.IMAGE_PATH + "screen/life.png").convert()
		bomb = pygame.image.load(self.c.IMAGE_PATH + "screen/bomb.png").convert()
		power = pygame.image.load(self.c.IMAGE_PATH + "screen/power.png").convert()
		clock = pygame.image.load(self.c.IMAGE_PATH + "screen/clock.png").convert()

		self.blit(player,(40,650))
		self.blit(clock,(365,650))

		self.blit(bomb,(590,647))
		self.blit(power,(670,650))
		self.blit(life,(740,652))

	def initPlayers(self):
		"""
		Place players
		"""
		if self.mode == self.c.SINGLE:
			self.user = player.Player("Player 1","p_1_",0,(40,40))
			self.players.append(self.user)
			self.blit(self.user.image, self.user.position)
		elif self.mode == self.c.MULTI:
			for p in self.players:
				if str(p.id) == str(self.id):
					self.user = p
				self.blit(p.image,p.position)

	def initEnemies(self, num):
		"""
		Generate enemies in semi-random positions around board
		Will not spawn near player
		"""
		for i in range(0,num):
			while True:
				x = random.randint(6,self.field.width-2)*40
				y = random.randint(6,self.field.height-2)*40

				if self.field.getTile((x,y)).canPass() == True:
					break

			e = enemy.Enemy("Enemy", "e_%d_" % (random.randint(1,self.c.MAX_ENEMY_SPRITES)), (x,y))
			self.enemies.append(e)
			self.blit(e.image, e.position)

	def runGame(self):
		"""
		Cycling and updating of all the game states and variables
		"""
		clock = pygame.time.Clock()
		pygame.time.set_timer(pygame.USEREVENT,1000)
		pygame.time.set_timer(pygame.USEREVENT+1,500)
		cyclicCounter = 0

		#Begin game
		self.gameIsActive = True
		self.auto = False

		#Save human playing data to csv file for model training
		classw = NNClass.myClassifier('fakeEnemysFull.csv', "./ENEMYSCONFIGFULL")
		classw.trainModel(0)
		classx = NNClass.myClassifier('fakeWallsFull.csv', "./WALLSCONFIGFULL")
		classx.trainModel(0)
		classy = NNClass.myClassifier('fakeBricksFull.csv', "./BRICKSCONFIGFULL")
		classy.trainModel(0)
		classz = NNClass.myClassifier('fakeBombsFull.csv', "./BOMBSCONFIGFULL")
		classz.trainModel(0)

		while self.gameIsActive:
			clock.tick(self.c.FPS)
			self.checkPlayerEnemyCollision()
			self.checkWinConditions()

			#Feature extraction for machine learning
			grid = featureExtract.grid(self)

			# MULTIPLAYER
			if self.mode == self.c.MULTI:
				self.tcpUpdate()
				self.manipulateTcpData()

			# self.c.FPS is set to 30, 30 ticks = 1 second
			cyclicCounter += 1
			if cyclicCounter == self.c.FPS:
				cyclicCounter = 0
				self.updateTimer()

			if cyclicCounter%5 == 1:
				self.clearExplosion()
			for event in pygame.event.get():
				if self.auto:

					# generate full grid for feature extraction
					x = self.user.position[0] / self.c.TILE_SIZE
					y = self.user.position[1] / self.c.TILE_SIZE
					myMat = featureConvert.convertGrid(np.matrix(self.user.map.matrix).transpose(), (x,y) ,21,17)
					action_tot = []
					action_list = [] # array of all the actions

					# append player action to the end of converted grid feature
					converted, info = prepSave.convertFiles(myMat,0)
					action_number1 = classx.predict([converted + [self.user.currentBomb,self.user.power]])
					action_list.append(action_number1)
					if(info[0] < 10):
						converted, info = prepSave.convertFiles(myMat,2)
						action_number2 = classz.predict([converted + [self.user.currentBomb,self.user.power]])
						action_list.append(action_number2)
					else:
						action_list.append([0,0,0,0,0,0])
					if(info[1] < 10):
						converted, info = prepSave.convertFiles(myMat,3)
						action_number3 = classw.predict([converted + [self.user.currentBomb,self.user.power]])
						action_list.append(action_number3)
					else:
						action_list.append([0,0,0,0,0,0])
					if(info[0] >= 10 and info[1] >= 10):
						converted, info = prepSave.convertFiles(myMat,1)
						action_number4 = classy.predict([converted + [self.user.currentBomb,self.user.power]])
						action_list.append(action_number4)
					else:
						info[2] = 10
						action_list.append([0,0,0,0,0,0])
					info = [2] + info
					for i in range(len(info)):
						info[i] = 10 - info[i]
					sumInfo = sum(info)
					for i in range(len(info)):
						info[i] = info[i]/sumInfo
					for i in range(len(action_number1)):
						tot = 0
						for j in range(len(action_list)):
								tot += action_list[j][i]*info[j]
						action_tot.append(tot)
					print(info)

					action_tot[1] += 1 - sum(action_tot)
					print(action_tot)
					action_number = np.random.choice(np.arange(0, 6), p=action_tot)
					print(action_number)
					if action_number in [1,2,3,4]:
						pred_move = self.move_dict[action_number]
						point = self.user.movement(pred_move,grid,2)
						self.movementHelper(self.user,point)
					elif action_number == 5:
						self.deployBomb(self.user)
				if event.type == pygame.QUIT:
					self.forceQuit()
				elif event.type == pygame.KEYDOWN:
					#On button press
					k = event.key
					#Switch to computer controlled human
					if k == pygame.K_RSHIFT:
						# alter between normal and AI mode
						self.auto = not self.auto
					elif k == pygame.K_SPACE and not self.auto:
						if self.mode == self.c.MULTI:
							self.sendingData = ["update","bomb",k,self.id]
						self.deployBomb(self.user)
					elif k == pygame.K_ESCAPE and not self.auto:
						# Restart the game when you are running on manual mode
						# by pressing esc"
						print("game restarts in 1 second")
						time.sleep(1)
						self.restart()
					elif (k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT) and not self.auto:
						if self.mode == self.c.MULTI:
							self.sendingData = ["update","movement",k,self.id]
						# player's move method when in normal mode
						point = self.user.movement(k,grid,0) # next point
						self.movementHelper(self.user, point)

					#Cheat mode, get powerups
					elif k == pygame.K_g and not self.auto:
						self.user.gainPower(self.c.BOMB_UP)
						self.user.gainPower(self.c.POWER_UP)

				elif event.type == pygame.USEREVENT: # RFCT - change definition
					self.updateBombs()
				elif event.type == pygame.USEREVENT+1: #RFCT
					for e in self.enemies:
						self.movementHelper(e,e.nextMove(grid))
					#Character motion set to enemy cycles
					if self.mode == self.c.MULTI:
						self.sendingData = ["update","movement",pygame.K_BACKSPACE,self.id]

				self.updateDisplayInfo()
				pygame.display.update()

	def deployBomb(self,player):
		"""
		Placing of bombs based

		Additional code written so machine learning can
		recognize if it is standing on a bomb as usually player
		overwrites bomb
		"""
		b = player.deployBomb() # Returns a bomb if available
		x = player.position[0] / self.c.TILE_SIZE
		y = player.position[1] / self.c.TILE_SIZE
		myMat = featureConvert.convertGrid(np.matrix(player.map.matrix).transpose(), (x,y) ,21,17)
		if not self.auto:
			# deploy bomb when in normal mode
			added = [player.currentBomb,player.power,5]
			tempGrid, info = prepSave.convertFiles(myMat,0)
			prepSave.saveFiles(tempGrid,added,0)
			if info[1]>=4:
				prepSave.saveFiles(prepSave.convertFiles(myMat,1)[0],added,1)
			if(info[0]!=10):
				prepSave.saveFiles(prepSave.convertFiles(myMat,2)[0],added,2)
			if(info[1]!=10):
				prepSave.saveFiles(prepSave.convertFiles(myMat,3)[0],added,3)
		if b != None:
			tile = self.field.getTile(player.position)
			tile.bomb = b
			self.bombs.append(b)


	def blit(self,obj,pos):
		self.screen.blit(obj,pos)
	#	pygame.display.flip()

	def movementHelper(self, char, point):
		"""
		Moves player in code
		"""
		nPoint = char.position.move(point)

		tile = self.field.getTile(nPoint)

		# Check for bomb / special power ups here
		if tile.canPass():
			if char.instance_of == 'player' and tile.isPowerUp():
				char.setScore(50) # RFCT | BUG - VARIES DEPENDING ON POWER UP
				char.gainPower(tile.type)
				tile.destroy()
				self.blit(tile.getBackground(),nPoint)
			char.move(point)

			self.blit(char.image, char.position)

			t = self.field.getTile(char.old)
			if t.bomb != None:
				self.blit(t.getBackground(),char.old)
			self.blit(t.getImage(), char.old)

	def updateBombs(self):
		"""
		Countdown bombs, explode if needed
		"""
		for bomb in self.bombs:
			if bomb.tick() == 0:
				self.activateBomb(bomb)

	def activateBomb(self,bomb):
		"""
		Remove bomb, kill surroundings
		"""
		if not bomb.triggered:
			bomb.explode()
			self.triggerBombChain(bomb)
			self.bombs.remove(bomb)
			tile = self.field.getTile(bomb.position)
			tile.bomb = None
			self.blit(tile.getImage(), bomb.position)
			self.resetTiles.append(bomb.position)

			explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
			self.blit(explosion,bomb.position)

	def triggerBombChain(self, bomb):
		"""
		Allow for bombs to activate other bombs
		"""
		if bomb == None:
			return
		else:
			bomb.triggered = True
			self.bombHelper(bomb,'left')
			self.bombHelper(bomb,'right')
			self.bombHelper(bomb,'up')
			self.bombHelper(bomb,'down')
			self.checkPlayerEnemyBombCollision(bomb.position)

	def bombHelper(self, bomb, direction):
		#Runs the code behind bomb explosions
		if direction == 'right':
			point = (40,0)
		elif direction == 'left':
			point = (-40,0)
		elif direction == 'up':
			point = (0,-40)
		elif direction == 'down':
			point = (0,40)

		x = y = 0
		while True:
			x += point[0]
			y += point[1]

			nPoint = bomb.position.move((x,y))
			t = self.field.getTile(nPoint)
			# hit a block or indestructible object
			if not t.canBombPass():
				# trigger new bomb explosion
				if t.bomb != None:
					self.activateBomb(t.bomb)
				elif t.destroyable == True:
					# if brick or powerup or player
					t.destroy()
					self.blit(t.getImage(),nPoint)
					self.user.setScore(10)
				break
			else:
				# path which explosion can travel on
				self.checkPlayerEnemyBombCollision(nPoint)

				explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
				self.blit(explosion,nPoint)
				self.resetTiles.append(nPoint)

			# check bomb's power, this terminates the recursive loop
			if int(abs(x)/40) == bomb.range or int(abs(y)/40) == bomb.range:
				#	print "(x,y) => (" + str(x) + "," + str(y) + ")"
				break

	def clearExplosion(self):
		"""
		Update board accordingly to bomb's effect
		"""
		for point in self.resetTiles:
			t = self.field.getTile(point)
			self.blit(t.getImage(),point)
			self.resetTiles.remove(point)

	def resetPlayerPosition(self, player, death):
		"""
		Put player back in top left on death or level clear
		"""
		player.reset(death)
		self.blit(player.image,player.position)

	def checkPlayerEnemyBombCollision(self, position):
		"""
		Check bomb's effects against player and enemy positions and clear
		if need be
		"""
		for player in self.players:
			if player.position == position:
				if player.loseLifeAndGameOver():
					self.gameover(player)
				else:
					# if the player gets hit by a blast, reset it's position to the starting position and reduce the score
					player.setScore(-100)
					self.resetPlayerPosition(player,True)

		# check if enemy was hit by bomb
		for enemy in self.enemies:
			if enemy.position == position:
				self.enemies.remove(enemy)
				self.user.setScore(100)

	def checkPlayerEnemyCollision(self):
		"""
		Check if enemy has killed player
		"""
		for enemy in self.enemies:
			if enemy.position == self.user.position:
				# RFCT - code repetition
				if self.user.loseLifeAndGameOver():
					self.gameover(self.user)
				self.user.setScore(-250)
				self.resetPlayerPosition(self.user,True)

	def checkWinConditions(self):
		if self.mode == self.c.SINGLE:
			if len(self.enemies) == 0:
				self.victory()

	def gameover(self, player):
		if self.mode == self.c.SINGLE:
			print('gameover - lost all lives | or time ran out')
			self.highscores.addScore(player.score)
			self.gameIsActive = False
			self.exitGame = True

			print("restarting in 3 second")
			time.sleep(1)
			print("restarting in 2 second")
			time.sleep(1)
			print("restarting in 1 second")
			time.sleep(1)
			self.restart()

	def fQuit(self):
		self.gameIsActive = False
		self.exitGame = True
		self.forceQuit = True


	def restart(self):
		"""
		This function forces the game to go back to its initial state
		"""
		self.firstRun = True
		self.resetGame()
		self.clearBackground()
		self.initGame()

	def printText(self,text,point):
		font = pygame.font.Font("lucida.ttf",20)
	#	font = pygame.font.SysFont("resources/fonts/Lucida Console",26)
		label = font.render(str(text)+'  ', True, (255,255, 255), (0, 0, 0))
		textRect = label.get_rect()
		textRect.x = point[0]
		textRect.y = point[1]
		self.blit(label, textRect)

	def victory(self):
		self.gameIsActive = False
		self.user.setScore(500)
		self.level += 1
		if self.level > 6:
			self.stage += 1
			self.level = 1
		mp = music.Music()
		mp.playSound("victory")
		time.sleep(2)

	def updateTimer(self):
		self.timer -= 1

		# user lost
		if self.timer == 0:
			self.gameover(self.user)

		mins = str(int(self.timer/60))
		secs = str(int(self.timer%60))

		if len(mins) == 1:
			mins = "0"+mins
		if len(secs) == 1:
			secs = "0"+secs
		txt = "%s:%s" % (mins,secs)
		self.printText(txt,(400,653))
