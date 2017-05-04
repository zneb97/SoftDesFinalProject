"""
This module contains functions that convert a grid list into a 2-D numpy array.
The grid list contains all instances of the current game.
The player location is always fixed on the center of the matrix by
appendeding zeros that shift automatically in accordance with the player
movment. This was a technical choice made to reduce the time complexity.


Project : Bomberman Bot with Machine Learning
Olin College Software Design Final Orject,  Spring 2017
By : TEAM AFK
"""

import numpy as np


def convertGrid(grid, pPos, viewX, viewY):
    """
    Converts a 2d grid list into a numpy array, appended with zeros
    so that the player is always located at its center.
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
