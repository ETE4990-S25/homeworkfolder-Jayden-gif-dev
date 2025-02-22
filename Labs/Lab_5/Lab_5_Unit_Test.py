
## Lab 5 - Unit Testing Partner Code
import unittest
class Demon:
    def __init__(self, name, demon_type):
        self.name = name
        self.demon_type = demon_type.lower()
        self.set_attribute()
    
    def set_attribute(self):
        if self.demon_type == "goblin":
            self.health = 80
            self.attack = 120
        elif self.demon_type == "lucifer":
            self.health = 120
            self.attack = 50
        elif self.demon_type == "aamon":
            self.health = 90
            self.attack = 70
        else:
            raise ValueError("Invalid demon type")
        
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"{self.name} ({self.demon_type.capitalize()} Demon) - Health: {self.health}, Attack: {self.attack}")

    def attack_target(self, target):
        print(f"{self.name} attacks {target.name} for {self.attack} damage!")
        target.take_damage(self.attack)

## Unit Test Begins

class TestDemon(unittest.TestCase):
    def test_initialization(self): ##This test case is to test the initialization of the Demon class
        demon = Demon("Bebu", "goblin") ##Creating a goblin object named Bebu
        self.assertEqual(demon.health, 80) ##Checking if the health of the goblin is 80
        self.assertEqual(demon.attack, 120) ##Checking if the attack of the goblin is 120

    def test_invalid_demon_type(self):
        with self.assertRaises(ValueError): ##Checking when the demon type is invalid
            Demon("Invalid demon type", "phantom") ##Checking if raises ValueError is what we expect
    
    def test_attack_target(self):
        attacker = Demon("Luc", "lucifer") ##Creating a Lucifer demon object named Luc that attacks the target
        target = Demon("Phong", "goblin")  ##Creating a goblin object named Phong that is the target
        attacker.attack_target(target) ##Lucifer demon attacks the goblin
        self.assertEqual(target.health, 30) # 80 - 50 = 30 Since goblin have 80 takes 50 damage from Lucifer demon's type

if __name__ == "__main__":
    unittest.main()