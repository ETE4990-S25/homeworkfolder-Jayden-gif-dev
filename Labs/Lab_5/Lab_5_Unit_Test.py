
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
    def test_initialization(self):
        goblin = Demon("Goblin", "goblin")
        self.assertEqual(goblin.health, 80)
        self.assertEqual(goblin.attack, 120)

    def test_invalid_demon_type(self):
        with self.assertRaises(ValueError):
            Demon("Invalid demon type", "phantom")
    
    def test_attack_target(self):
        attacker = Demon("Luc", "lucifer")
        target = Demon("Phong", "goblin")
        attacker.attack_target(target)
        self.assertEqual(target.health, 30) # 80 - 50 = 30 Since goblin have 80 takes 50 damage from Lucifer demon's type

if __name__ == "__main__":
    unittest.main()