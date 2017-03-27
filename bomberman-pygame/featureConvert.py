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
	buckets = [ [0] * resultGridX ] * resultGridY
	mymat = matrix(buckets)
	x = 0
	y = 0
	for i in range(grid.shape[0] - pPos[0], 2 * grid.shape[0] - pPos[0]):
		for j in range(grid.shape[1] - pPos[1], 2 * grid.shape[1] - pPos[1]):
			mymat.itemset( (i, j) , grid.item((x, y)) )
			print(str(i) + str(j))
			y += 1
		x += 1
		y = 0

	for i in range(0, mymat.shape[1]):
		for j in range(0, mymat.shape[0]):
			print mymat.item((j,i)),
		print "    "



if __name__ == '__main__':
	mygrid = [ [1] * 10 ] * 5
	convertGrid(matrix(mygrid), (1,1))
