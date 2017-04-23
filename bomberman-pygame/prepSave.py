import saveChoices
from numpy import matrix
import NNTest.predictSplit as predictSplit
fileNames = ['wallsFULL.csv','bricksFULL.csv','bombsFULL.csv','enemysFULL.csv']
# fieldnames = ['above','left', 'right', 'below','response']
fileDict = {'wallsFULL.csv' : 1,'bricksFULL.csv' : 2,'bombsFULL.csv' : 9,'enemysFULL.csv':7}

def convertFiles(myMat, x):
    '''this is gonna take the array of places and the move and save them to csv files for later use'''
    listPlaces = []
    position = (20,16)
    starty=12
    endy= 21#myMat.shape[1]
    startx=16
    endx=25#myMat.shape[0]
    info = [10,10,10]
    for i in range(starty,endy):
        for j in range(startx,endx):
            listPlaces.append(myMat.item((j,i)))
            if myMat.item((j,i)) == 9:
                dist = abs(20-j)+abs(16-i)
                if(info[0] == 10):
                    info[0] = dist
                elif(info[0]>dist):
                    info[0] = dist
            elif(myMat.item((j,i)) == 7):
                dist = abs(20-j)+abs(16-i)
                if(info[1] == 10):
                    info[1] = dist
                elif(info[1]>dist):
                    info[1] = dist
            elif(myMat.item((j,i)) == 2):
                dist = abs(20-j)+abs(16-i)
                if(info[2] == 10):
                    info[2] = dist
                elif(info[2]>dist):
                    info[2]= dist



    if(len(listPlaces) == 0):
        return

    '''this part builds a list for each instance and will add a 1 or 0 depending of the presence of the object'''
    tempList = []
    for j in range(len(listPlaces)):
        if(listPlaces[j] == fileDict[fileNames[x]]):
            tempList.append(1)
        elif(x == 0 and (listPlaces[j] == 2 or listPlaces[j] == 7)):
            tempList.append(1)
        elif(x == 3 and listPlaces[j] == 8):
            tempList.append(1)
        else:
            tempList.append(0)
    # if(fileNames[i]=='walls.csv'):
    #     classifier.predict([tempList])
    return tempList,info

def saveFiles(tempList, info, i):
    tempList = tempList + info
    saveChoices.addRow(fileNames[i],tempList)
