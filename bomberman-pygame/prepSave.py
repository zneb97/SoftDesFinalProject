import saveChoices
from numpy import matrix
import NNTest.predictSplit as predictSplit
fileNames = ['walls.csv','bricks.csv','bombs.csv']
fieldnames = ['above','left', 'right', 'below','response']
fileDict = {'walls.csv' : 1,'bricks.csv' : 2,'bombs.csv' : 9}

def convertFiles(myMat, x):
    '''this is gonna take the array of places and the move and save them to csv files for later use'''
    listPlaces = []
    starty=14
    endy=19#mymat.shape[1]
    startx=18
    endx=23#mymat.shape[0]
    info = [0]
    for i in range(starty,endy):
        for j in range(startx,endx):
            listPlaces.append(myMat.item((j,i)))
            if myMat.item((j,i)) == 9:
                info[0] = 1



    if(len(listPlaces) == 0):
        return

    '''this part builds a list for each instance and will add a 1 or 0 depending of the presence of the object'''
    tempList = []
    for j in range(len(listPlaces)):
        if(listPlaces[j] == fileDict[fileNames[x]]):
            tempList.append(1)
        elif(fileNames[x]=='walls.csv' and listPlaces[j] == 2):
            tempList.append(1)
        else:
            tempList.append(0)
    # if(fileNames[i]=='walls.csv'):
    #     classifier.predict([tempList])
    return tempList,info

def saveFiles(tempList, move, i):
    tempList.append(move)
    saveChoices.addRow(fileNames[i],tempList)
