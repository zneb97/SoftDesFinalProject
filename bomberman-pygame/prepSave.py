import saveChoices
fileNames = ['walls.csv','bricks.csv','bombs.csv']
fieldnames = ['above','left', 'right', 'below','response']
fileDict = {'walls.csv' : 1,'bricks.csv' : 2,'bombs.csv' : 9}

def saveFiles(listPlaces, move):
    '''this is gonna take the list of places and the move and save them to csv files for later use'''
    if(len(listPlaces) == 0):
        return
    for i in range(len(fileNames)):
        '''this part builds a list for each instance and will add a 1 or 0 depending of the presence of the object'''
        tempList = []
        for j in range(len(listPlaces)):
            if(listPlaces[j] == fileDict[fileNames[i]]):
                tempList.append(1)
            else:
                tempList.append(0)
        tempList.append(move)
        saveChoices.addRow(fileNames[i],tempList)
