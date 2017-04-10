import config as c
from numpy import matrix
import featureConvert

TILE_MAP = {0: 0,  # Ground -> 0()
            1: 1,  # Ground -> 0()
            2: 2,  # Ground -> 0()
            3: 3,  # Ground -> 0()
            4: 4}  # Ground -> 0()


class grid:
    """
    Identifies player, enemy, object positons from board

    Matrix Tile Code

    0 = VALID SPACE
    1 = WALL
    2 = BRICK
    3 = SECRET BRICK
    4 = SECRET BRICK

    7 = ENIMIES
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

    def __init__(self, game):
        """
        Initialize grid object
        """
        self.g = game
        self.field = game.field
        self.players = game.players
        self.bombs = game.bombs
        self.enemies = game.enemies
        self.matrix = self.initMatrix()

    def initMatrix(self):
        """
        Create base matrix and fill in
        """
        global TILE_MAP
        mat = []
        for row in self.field.board:
            mat_row = []
            for tile in row:
                mat_row.append(TILE_MAP[tile.type])
            mat.append(mat_row)
        self.add_players(mat)
        self.add_enemies(mat)
        self.add_bombs(mat)
        return mat

    def add_bombs(self, target_matrix):
        """
        Identify bomb objects on the board and add to grid
        """
        for bomb in self.bombs:
            x = int(bomb.position[0] / c.Config.TILE_SIZE)
            y = int(bomb.position[1] / c.Config.TILE_SIZE)
            target_matrix[y][x] = 9

    def add_players(self, target_matrix):
        """
        Identify players on the board and add to grid
        """
        # player.position / config.TILE_SIZE
        # update (x,y) with 8
        for player in self.players:
            x = int(player.position[0] / c.Config.TILE_SIZE)
            y = int(player.position[1] / c.Config.TILE_SIZE)
            target_matrix[y][x] = 8

    def add_enemies(self, target_matrix):
        """
        Identify enemies on the board and add to grid
        """
        for enemy in self.enemies:
            x = int(enemy.position[0] / c.Config.TILE_SIZE)
            y = int(enemy.position[1] / c.Config.TILE_SIZE)
            target_matrix[y][x] = 7

    def printMatrix(self):
        """
        Pad, center, and print matrix
        """
        x = self.players[0].position[0] / c.Config.TILE_SIZE
        y = self.players[0].position[1] / c.Config.TILE_SIZE
        featureConvert.convertGrid(matrix(self.matrix).transpose(), (x,y) ,21,17)
