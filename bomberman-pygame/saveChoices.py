import csv

def writeHead(fileName):
    with open(fileName, newline='') as csvfile:
         reader = csv.reader(csvfile, quotechar='|')
         numrows = 0
         for row in reader:
             numrows += 1
         print(numrows)
    with open(fileName, 'a') as csvfile:
        fieldnames = [str(numrows-1)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

def addRow(fileName, listInfo):
    with open(fileName, 'a') as csvfile:
        writer = csv.writer(csvfile,
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(listInfo)

def readCSV(fileName):
    with open('names.csv', newline='') as csvfile:
         spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
         for row in spamreader:
             print(', '.join(row))

def rewrite(fileName):
    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[])
        writer.writeheader()
#
# writeHead('bricks.csv')
# writeHead('walls.csv')
# writeHead('bombs.csv')
# rewrite('bricks.csv')
# rewrite('walls.csv')
# rewrite('bombs.csv')
