import saveChoices
from numpy import matrix
fileNames = ['walls.csv','bricks.csv','bombs.csv']
fieldnames = ['above','left', 'right', 'below','response']
fileDict = {'walls.csv' : 1,'bricks.csv' : 2,'bombs.csv' : 9}

def convertFeature(myMat, mat_type):
    tempList = []
    for j in range(len(myMat)):
        if(myMat[j] == mat_type):
            tempList.append(1)
        else:
            tempList.append(0)
    return(tempList)

def saveFiles(myMat, move):
    for i in range(len(fileNames)):
        '''this part builds a list for each instance and will add a 1 or 0 depending of the presence of the object'''
        tempList = convertFeature(myMat, fileDict[fileNames[i]])
        tempList.append(move)
        saveChoices.addRow(fileNames[i],tempList)
