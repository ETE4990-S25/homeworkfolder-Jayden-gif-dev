#Project 1
#Player as class with example usage.
class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class.lower()
        self.set_attributes()
    
    def set_attributes(self):
        if self.player_class == "mage":
            self.health = 80
            self.mp = 120
        elif self.player_class == "warrior":
            self.health = 120
            self.mp = 50
        elif self.player_class == "thief":
            self.health = 90
            self.mp = 70
        else:
            raise ValueError("Invalid class. Choose from: mage, warrior, thief.")
    
    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        print(f"{self.name} took {amount} damage. Health: {self.health}")
    
    def use_mana(self, amount):
        if self.mp >= amount:
            self.mp -= amount
            print(f"{self.name} used {amount} MP. MP left: {self.mp}")
        else:
            print(f"Not enough MP!")
    
    def __str__(self):
        return f"{self.name} ({self.player_class.capitalize()}) - Health: {self.health}, MP: {self.mp}"

# Example usage
player1 = Player("Arthas", "warrior")
print(player1)
player1.take_damage(30)
player1.use_mana(20)


#Example usage