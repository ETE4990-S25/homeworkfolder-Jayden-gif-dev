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

def displayJson(fileName):
    try:
        with open(fileName, 'r') as file:
            data = json.load(file)
            for student in data:
                print(student)
    except FileNotFoundError:
        print("File not found")

if __name__ == "__main__":
    students = [
        Student(fake.name(), fake.random_int(min=18, max=30), fake.email(), fake.random_int(min=1000, max=9999)).toJson()
        for _ in range(5)
    ]
    