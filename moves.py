from random import randint
import math
from pokemon import Pokemon, get_natures

class Move:
    max_pp = 10
    power = 80
    category = "special"
    move_type = "Water"
    def __init__(self):
        self.pp = self.max_pp

    def attack(self, user, target):
        random = randint(85, 100) / 100
        stab = 1
        if self.move_type in user.type:
            stab = 1.5

        if self.category == "special":
            attack = user.stats[3]
            defense = target.stats[4]

        elif self.category == "physical":
            attack = user.stats[1]
            defense = target.stats[2]

        modifier = stab * random

       #https://bulbapedia.bulbagarden.net/wiki/Damage 

        damage = math.floor(((( (((2 * user.level) / 5) + 2) * self.power * (attack / defense)) / 50) + 2) * modifier)
        self.pp -= 1
        target.hp -= damage

move = Move()
user = Pokemon("Registeel", [80,75,150,75,150,50], ["Steel"])
user.change_nature("Sassy")
target = Pokemon("Registeel", [80,75,150,75,150,50], ["Steel"])
target.change_nature("Sassy")

print(user.stats)
print(target.stats)

move.attack(user, target)

print(user.hp)
print(target.hp)
damage = target.stats[0] - target.hp
print(damage)
print(damage * 100 / target.stats[0])

