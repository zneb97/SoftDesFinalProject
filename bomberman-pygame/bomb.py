import config, pygame, character

class Bomb(pygame.sprite.Sprite):
	fuse = 3

	def __init__(self,player):
		"""
		Intialize a bomb object

		Takes in player to evantually return bomb to them
		as well as get positions for when placing bomb.
		"""
		pygame.sprite.Sprite.__init__(self)
		self.c = config.Config()

		self.image = pygame.image.load(self.c.IMAGE_PATH + "bomb.png").convert()
		self.position = self.image.get_rect()
		self.position = self.position.move((player.position.x,player.position.y))
		self.range = player.power
		self.player = player
		self.triggered = False

	def tick(self):
		"""
		Countdown until explosion

		Note: explosion hadnled in game
		"""
		self.fuse -= 1
		return self.fuse

	def explode(self):
		"""
		Bomb returns to player
		"""
		self.player.currentBomb += 1
