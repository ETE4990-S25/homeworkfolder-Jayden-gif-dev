#Import
import os

#Simple reading the file and returning the list of lines
def readFile(filePath):
    with open(filePath, 'r') as file:
        return file.readlines()
#Validates if the given file path exists and raises an exception if it does not.
def validateFilePath(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"Error: The file '{filePath}' was not found.")
    return filePath


## I need to convers a list of lines into a dictionary mapping numbers to words.
## Each line is expected to contain a number followed by a word.
def parseLines(lines):
    numWordMap = {}
    for line in lines:
        parts = line.strip().split()
        if len(parts) == 2:
            numWordMap[int(parts[0])] = parts[1]
        return numWordMap

##I need to determines the pyramid positions by computing which numbers should be used based on the pyramids structure.
def determinePyramidPositions(numWordMap):
    pyramidPositions = []
    row, num = 1, 1
    while num in numWordMap:
        pyramidPositions.append(num)
        row += 1
        num += row + 1
    return pyramidPositions


    
        