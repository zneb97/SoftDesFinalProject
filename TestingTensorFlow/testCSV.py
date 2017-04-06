import csv
fieldnames = ['above','left', 'right', 'below','response']

def writeHead(fileName):
    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def addRow(fileName, listInfo):
    rowDict = {}
    for i in range(len(fieldnames)):
        rowDict[fieldnames[i]] = listInfo[i]
    with open(fileName, 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(rowDict)

def readCSV(fileName):
    with open('names.csv', newline='') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
         for row in spamreader:
             print(', '.join(row))


writeHead('names.csv')
addRow('names.csv',['1','1','0','1'])
addRow('names.csv',['1','1','0','1'])
readCSV('names.csv')
