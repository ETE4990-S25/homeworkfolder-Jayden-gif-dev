#Import
import os

def readFile(filePath):
    with open(filePath, 'r') as file:
        return file.readlines()
    
def validateFilePath(filePath):
    if not os.path.exists(filePath):
        raise FileNotFoundError(f"Error: The file '{filePath}' was not found.")
    return filePath