"""takes in the grid and player positions

Matrix Tile Code

0 = VALID SPACE
1 = WALL
2 = BRICK
3 = SECRET BRICK (BOMB_UP)
4 = SECRET BRICK (POWER_UP)
6 = REVEALED BOMB_UP
7 = REVEALED POWER_UP

8 = PLAYERS
9 = BOMBS


Original Game Tile Code
GROUND = 0
WALL = 1
BRICK = 2
BOMB_UP = 3
POWER_UP = 4
LIFE_UP = 5
TIME_UP = 6

"""
import config as c
from numpy import matrix
import featureConvert

TILE_MAP = {0: 0,  # Ground -> 0()
            1: 1,  # Ground -> 0()
            2: 2,  # Ground -> 0()
            3: 3,  # Ground -> 0()
            4: 4}  # Ground -> 0()


class grid:

    def __init__(self, game):
        self.g = game
        self.field = game.field
        self.players = game.players
        self.bombs = game.bombs
        self.matrix = self.initMatrix()

    def initMatrix(self):
        global TILE_MAP
        mat = []
        for row in self.field.board:
            mat_row = []
            for tile in row:
                mat_row.append(TILE_MAP[tile.type])
            mat.append(mat_row)

        self.add_bombs(mat)
        self.add_players(mat)
        return mat

    def add_bombs(self, target_matrix):
        # bomb.position (x,y) / config.TILE_SIZE
        # update (x,y) with 9
        for bomb in self.bombs:
            x = int(bomb.position[0] / c.Config.TILE_SIZE)
            y = int(bomb.position[1] / c.Config.TILE_SIZE)
            target_matrix[y][x] = 9

    def add_players(self, target_matrix):
        # player.position / config.TILE_SIZE
        # update (x,y) with 8
        for player in self.players:
            x = int(player.position[0] / c.Config.TILE_SIZE)
            y = int(player.position[1] / c.Config.TILE_SIZE)
            target_matrix[y][x] = 8

    def printMatrix(self):
        for row in self.matrix:
            s = ''
            for col in row:
                s += str(col)
            print(s)
        print("\n")

    def printPlayerView():
        """probably doesnt work"""
        x = self.players[0].position[0] / c.Config.TILE_SIZE
        y = self.players[0].position[1] / c.Config.TILE_SIZE
        featureConvert.convertGrid(matrix(self.matrix), (x,y) ,21,17)
