"""
This module Extracts features (player, enemy, bombs) from the main game loop
and stores the data as a two-demensional list

Project : Bomberman Bot with Machine Learning
Olin College Software Design Final Orject,  Spring 2017
By : TEAM AFK
"""


import config as c


class grid:
    """
    Tile Code:
    0 = VALID SPACE, 1 = WALL, 2 = BRICK, 3 = SECRET BRICK, 4 = SECRET BRICK
    7 = ENIMIES, 8 = PLAYERS, 9 = BOMBS
    """

    def __init__(self, game):
        """
        Initlizes the attributes that represent the grid status
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
        A 2-d list(matrix) of players, enemies, and bombs on the grid
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
