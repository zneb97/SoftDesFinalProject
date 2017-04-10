import config as c
from numpy import matrix
import featureConvert


class grid:
    """
<<<<<<< HEAD
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
    """
    def __init__(self, game):
        """
        Thie function initlizes the attributes that represent the grid
        from the current game instance
        """
        self.g = game
        self.field = game.field
        self.players = game.players
        self.bombs = game.bombs
        self.enemies = game.enemies


    @property
    def matrix(self):
        """
        This property function returns the grid,
        with all players, enimies, and bombs added
        """
        mat = []
        for row in self.field.board:
            mat_row = []
            for tile in row:
                mat_row.append(tile.type)
            mat.append(mat_row)
        self.add_players(mat)
        self.add_enemies(mat)
        self.add_bombs(mat)
        return mat

    def add_bombs(self, target_matrix):
        """

        Adds bombs(represented as 9) to the target_matrix
        """
        # bomb.position (x,y) / config.TILE_SIZE
        # update (x,y) with 9
        for bomb in self.bombs:
            x = int(bomb.position[0] / c.Config.TILE_SIZE)
            y = int(bomb.position[1] / c.Config.TILE_SIZE)
            target_matrix[y][x] = 9

    def add_players(self, target_matrix):
        """
        Adds players(represented as 8) to the target_matrix
        """
        for player in self.players:
            x = int(player.position[0] / c.Config.TILE_SIZE)
            y = int(player.position[1] / c.Config.TILE_SIZE)
            target_matrix[y][x] = 8

    def add_enemies(self, target_matrix):
        """
        Adds enimies(represented as 7) to the target_matrix
        """
        for enemy in self.enemies:
            x = int(enemy.position[0] / c.Config.TILE_SIZE)
            y = int(enemy.position[1] / c.Config.TILE_SIZE)
            target_matrix[y][x] = 7

    def printMatrix(self):
        """
        This function calls the convert grid function,
        converts the list into a numpy matrix"
        """
        x = self.players[0].position[0] / c.Config.TILE_SIZE
        y = self.players[0].position[1] / c.Config.TILE_SIZE
        featureConvert.convertGrid(matrix(self.matrix).transpose(), (x,y) ,21,17)
