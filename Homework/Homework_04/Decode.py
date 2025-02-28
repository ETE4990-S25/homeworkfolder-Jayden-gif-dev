#Import
import os

def readFile(filePath):
    with open(filePath, 'r') as file:
        return file.readlines()