"""
Project : Bomberman Bot with Machine Learning
Olin College Software Design Final Orject,  Spring 2017
By : TEAM AFK

Takes in all player and objects places to create a grid.
This grid is appended by zeros and shifts automatically
to always locatled the player in the center to reduce computation complexity.

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

import numpy as np


def convertGrid(grid, pPos, viewX, viewY):
    """
    Paremeters :
    grid -> numpy matrix
    pPos -> Tuple of player Position (x, y)
    viewX : Number of columns of the original grid
    viewY : Number of rows of the original grid

    Output :
    An extended matrix appended with zeros so that the player is always
    located at the center
    """
    resultGridX = 2 * viewX - 1
    resultGridY = 2 * viewY - 1
    buckets = [[1] * resultGridY] * resultGridX
    mymat = np.array(buckets)
    x = 0
    y = 0
    for i in range(int(grid.shape[1] - pPos[1] - 1),
                   int(2 * grid.shape[1] - pPos[1] - 1)):
        for j in range(int(grid.shape[0] - pPos[0] - 1),
                       int(2 * grid.shape[0] - pPos[0] - 1)):
            mymat.itemset((j, i), grid.item((x, y)))
            x += 1
        y += 1
        x = 0
    printGrid(mymat)
    return mymat


def printGrid(mymat):
    """
    Prints the 5x5 matrix with the player located at the center.
    Serves as a testing code to see if the feature extraction is working.
    """
    mat = np.concatenate(([mymat[18][14:19]],
                          [mymat[19][14:19]],
                          [mymat[20][14:19]],
                          [mymat[21][14:19]],
                          [mymat[22][14:19]]),
                         axis=0)
    print(mat.T)
    print(" ")
