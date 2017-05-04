"""
This module reads and writes CSV files to save/load the training data.

Project : Bomberman Bot with Machine Learning
Olin College Software Design Final Orject,  Spring 2017
By : TEAM AFK
"""

import csv


def writeHead(fileName):
    '''
    Inserts the header into csv file.
    '''
    with open(fileName, newline='') as csvfile:
        reader = csv.reader(csvfile, quotechar='|')
        numrows = 0
        for row in reader:
            numrows += 1
        print(numrows)

    with open(fileName, 'a') as csvfile:
        # record the number of training data
        fieldnames = [str(numrows - 1)]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()


def addRow(fileName, listInfo):
    '''
    Adds a new row to the csv.
    '''
    with open(fileName, 'a') as csvfile:
        writer = csv.writer(csvfile,
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(listInfo)


def readCSV(fileName):
    """
    Loads the CSV file with the given filename
    """
    with open('names.csv', newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(', '.join(row))


def rewrite(fileName):
    """
    Overwrites the CSV file with the given filename
    """
    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=[])
        writer.writeheader()
