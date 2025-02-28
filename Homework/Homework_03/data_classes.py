#Import
import json
import os
from faker import Faker

# Create an instance of the Faker class to generate fake data
fake = Faker()

class Person:
    def __init__(self, Name, Age, Email):
        self.Name = Name
        self.Age = Age
        self.Email = Email
    
    def toJson(self):
        return {
            "Name": self.Name,
            "Age": self.Age,
            "Email": self.Email
        }

class Student(Person):
    def __init__(self, Name, Age, Email, StudentId):
        self.Name = Name
        self.Age = Age
        self.Email = Email
        self.StudentId = StudentId
    
    def toJson(self):
        return {
            "Name": self.Name,
            "Age": self.Age,
            "Email": self.Email,
            "StudentId": self.StudentId
        }

def saveToJson(fileName, students):
    filePath = os.path.join(os.getcwd(), fileName)  # Create full path in the current directory
    try:
        with open(filePath, "w") as file:
            json.dump([student.toJson() for student in students], file, indent=4)
        print(f"File saved at: {filePath}")
    except (OSError, IOError) as e:
        print(f"Error saving file: {e}")

def displayJson(fileName):
    filePath = os.path.join(os.getcwd(), fileName)
    try:
        with open(filePath, "r") as file:
            data = json.load(file)
            print(json.dumps(data, indent=4))
    except FileNotFoundError:
        print("File not found.")

if __name__ == "__main__":
    students = [
        Student(fake.name(), fake.random_int(min=18, max=30), fake.email(), fake.random_int(min=1000, max=9999))
        for _ in range(5)
    ]
    
    fileName = "students.json"
    saveToJson(fileName, students)
    displayJson(fileName)
