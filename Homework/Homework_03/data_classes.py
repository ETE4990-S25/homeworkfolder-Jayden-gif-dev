#Imports
import json

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
    with open(fileName, 'w') as file:
        json.dump(students, file, indent=4)