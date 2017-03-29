"""takes in the grid and player positions
-1 = Not real space
0 = valid space
1 = wall
2 = BRICK
3 = secret BRICK
4 = monster"""
from numpy import matrix

# def prepGrid(grid, pPos):
# 	viewX = 21
# 	viewY = 17
# 	convertGrid(grid, pPos, viewX, ViewY)

def convertGrid(grid, pPos, viewX, viewY):
	resultGridX = 2 * viewX - 1
	resultGridY = 2 * viewY - 1
	buckets = [ [0] * resultGridY ] * resultGridX
	mymat = matrix(buckets)
	x = 0
	y = 0
	for i in range(grid.shape[0] - pPos[0] - 1, 2 * grid.shape[0] - pPos[0] - 1):
		for j in range(grid.shape[1] - pPos[1] - 1, 2 * grid.shape[1] - pPos[1] - 1):
			mymat.itemset( (j, i) , grid.item((x, y)) )
			# print(str(i) + str(j))
			y += 1
		x += 1
		y = 0

	mymat.itemset((resultGridX/2, resultGridY/2), 8)

	for i in range(0, mymat.shape[1]):
		for j in range(0, mymat.shape[0]):
			print(mymat.item((j,i)), end=' ')
		print("    ")



if __name__ == '__main__':
	viewX = 21
	viewY = 17
	convertGrid(matrix(mygrid), (0,9), viewX, ViewY)
