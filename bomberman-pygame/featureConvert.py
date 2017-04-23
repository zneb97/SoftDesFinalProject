
import numpy as np

"""
Takes in all player and objects places to create a grid. This grid is padded
by 0s and shifts to keep player in the center to reduce computation

-1 = Not real space
0 = Valid space
1 = Wall
2 = BRICK
3 = Secret BRICK
4 = Monster

"""

def convertGrid(grid, pPos, viewX, viewY):
	resultGridX = 2 * viewX - 1
	resultGridY = 2 * viewY - 1
	buckets = [ [1] * resultGridY ] * resultGridX
	mymat = np.array(buckets)
	x = 0
	y = 0
	for i in range(int(grid.shape[1] - pPos[1] - 1), int(2 * grid.shape[1] - pPos[1] - 1)):
		for j in range(int(grid.shape[0] - pPos[0] - 1), int(2 * grid.shape[0] - pPos[0] - 1)):
			mymat.itemset( (j,i) , grid.item((x, y)) )
			x += 1
		y += 1
		x = 0
	printGrid(mymat)
	return mymat

def condense_matrix(mymat):
	# Hardcoded matrix condense algorithm, can improve in the future
	return np.concatenate((mymat[18][14:19],mymat[19][14:19],mymat[20][14:19],mymat[21][14:19],mymat[22][14:19]), axis=0)

def printGrid(mymat):
	"""
	Print out padded grid
	"""
	# Print the entire matrix
	# for i in range(0, mymat.shape[1]):
	# 	for j in range(0, mymat.shape[0]):
	# 		print(mymat.item((j,i)), end='')
	# 	print("    ")
	mat = np.concatenate(([mymat[18][14:19]],[mymat[19][14:19]],[mymat[20][14:19]],[mymat[21][14:19]],[mymat[22][14:19]]), axis=0)
	print(mat.T)
	print(" ")

if __name__ == '__main__':
	viewX = 21
	viewY = 17
	mygrid = [[1] * viewY] * viewX
	convertGrid(matrix(mygrid), (0,9), viewX, viewY)
