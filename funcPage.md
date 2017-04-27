---
title: Key Functions
layout: template
filename: funcPage
---
# Key Functions and Classes

## Grid Class

Located in featureExtract.py.

The gird class makes use of the predefined enemies, bombs, and players array, as well as the board and from that data creates a 2 dimensional array of numbers corresponding to different objects.

The game class already has a running list of bombs, characters, and enemies, and within each of those objects is positional data for where it is on the board. Iterating through these lists and pulling the data, we place the numbers representing the objects in the correct matrix coordinate in our new grid. The rest of the data is pulled from the board class already defined by the base game to fill in walls, bricks and walking paths.

This grid is then used to locate various objects in realtion to one another on the game screen.

## convertGrid(grid, pPos, viewX, viewY)

Located in featureConvert.py

It creates the previously explained grid class for the current game. It then pads this matrix with zeros. The placement of zeros around the grid is relative to the player's position, making sure the player is always in the center of the matrix. This is to cut down the run time of finding the player character in the matrix because it will always be at the same coordinate.
