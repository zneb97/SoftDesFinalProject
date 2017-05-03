"""
Project : Bomberman Bot with Machine Learning
Olin College Software Design Final Orject,  Spring 2017
This entire code was written by the original author, Rickyc (Github user)
No edits were done by the members of Team AFK
"""

import sys, pygame, config, game, highscore

class Titlescreen():

	def __init__(self):
		self.c = config.Config()
		exitMain = False

		while not exitMain:
			pygame.init()
			self.screen = pygame.display.set_mode((1028,768))
			pygame.display.set_caption("Bomberman")

			imagePath = self.c.IMAGE_PATH + "titlescreen.png"
			img = pygame.image.load(imagePath).convert()
			self.screen.blit(img,(0,0))

			pygame.mixer.music.load(self.c.AUDIO_PATH + "title.mid")
			pygame.mixer.music.play()

			clock = pygame.time.Clock()
			pygame.mouse.set_visible(True)
			pygame.display.flip()
			userInteracted = False

			while not userInteracted:
				clock.tick(self.c.FPS)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						userInteracted = True
						exitMain = True
						pygame.quit()
					elif event.type == pygame.KEYDOWN:
						if event.key == pygame.K_ESCAPE:
							userInteracted = True
							exitMain = True
							pygame.quit()
					elif event.type == pygame.MOUSEBUTTONDOWN:
						if self.withinBoundary(25, 250, 500, 540):
							userInteracted = True
							self.singlePlayer() # Single Player game clicked
						elif self.withinBoundary(25, 250, 550, 600):
							userInteracted = True
							self.highScores() # High Score clicked
						elif self.withinBoundary(25, 240, 605, 645):
							userInteracted = True
							exitMain = True
							pygame.quit() # Exit clicked

	def withinBoundary(self, x1, x2, y1, y2):
		if pygame.mouse.get_pos()[0] >= x1 and pygame.mouse.get_pos()[0] <= x2 and pygame.mouse.get_pos()[1] >= y1 and pygame.mouse.get_pos()[1] <= y2:
			return True
		return False

	def singlePlayer(self):
		g = game.Game(self.c.SINGLE)

	def multiplayer(self):
		g = game.Game(self.c.MULTI)

	def instructions(self):
		print("Instructions clicked!")

	def highScores(self):
		h = highscore.Highscore()
		h.displayScore()

	def clearBackground(self):
		bg = pygame.Surface(self.screen.get_size())
		bg = bg.convert()
		bg.fill((0,0,0))
		self.blit(bg,(0,0))

if __name__ == "__main__":
    t = Titlescreen()
