"""takes in the grid and player positions
-1 = Not real space
0 = valid space
1 = wall
2 = BRICK
3 = secret BRICK
4 = monster"""
from numpy import matrix
def convertGrid(grid, pPos):
	viewX = 10
	viewY = 5
	resultGridX = 2 * viewX - 1
	resultGridY = 2 * viewY - 1
	buckets = [ [0] * resultGridY ] * resultGridX
	mymat = matrix(buckets)
	x = 0
	y = 0
	for i in range(grid.shape[0] - pPos[0] - 1, 2 * grid.shape[0] - pPos[0] - 1):
		for j in range(grid.shape[1] - pPos[1] - 1, 2 * grid.shape[1] - pPos[1] - 1):
			mymat.itemset( (j, i) , grid.item((x, y)) )
			print(str(i) + str(j))
			y += 1
		x += 1
		y = 0

	mymat.itemset((resultGridX/2, resultGridY/2), 5)

	for i in range(0, mymat.shape[1]):
		for j in range(0, mymat.shape[0]):
			print mymat.item((j,i)),
		print "    "



if __name__ == '__main__':
	mygrid = [ [1] * 10 ] * 5
	convertGrid(matrix(mygrid), (0,9))
