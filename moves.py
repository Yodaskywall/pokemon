from random import randint
import math
import pickle
from pokemon import Pokemon, get_natures

with open("type_info", "rb") as file:
    types, type_effectiveness = pickle.load(file)


def effectiveness(move_type, target_type):
    eff = 1
    for t in target_type:
        i = types.index(t)
        eff *= type_effectiveness[move_type][i]
    return eff


class Move:
    max_pp = 10
    power = 80
    category = "special"
    move_type = "Normal"
    flinch = False
    priority = 0
    accuracy = 100
    name = "xd"
    def __init__(self):
        self.pp = self.max_pp

    def attack(self, user, target):
        if not target.protected:
            prob = randint(0,100)
            if self.accuracy >= prob:
                random = randint(85, 100) / 100
                stab = 1
                if self.move_type in user.type:
                    stab = 1.5

                if self.category.lower() == "special":
                    attack = user.stats[3]
                    defense = target.stats[4]

                elif self.category.lower() == "physical":
                    attack = user.stats[1]
                    defense = target.stats[2]

                eff = effectiveness(self.move_type, target.type)

                modifier = stab * random * eff

               #https://bulbapedia.bulbagarden.net/wiki/Damage 

                damage = math.floor(((( (((2 * user.level) / 5) + 2) * self.power * (attack / defense)) / 50) + 2) * modifier)
                self.pp -= 1
                target.hp -= damage


class Protect(Move):
    category = "Status"
    accuracy = 100
    max_pp = 16
    priority = 4
    name = "Protection"
    def __init__(self):
        super().__init__()
    def attack(self, user, target):
        if user.protected_last_turn:
            if randint(1,100) > 50:
                user.protected = True
                print(f"{user.name} used protection.")
        else:
            user.protected = True
            print(f"{user.name} used protection.")


CUSTOM_MOVES = {
            "Protect" : Protect(),
        }

class Fake_Out(Move):
    max_pp = 16
    move_type = "Normal"
    power = 40
    category = "physical"
    flinch = True
    priority = 1
    def __init__(self):
        super().__init__()

    def attack(self, user, target):
        if user.first_turn:
            super().attack(user, target)

class Grassy_Slide(Move):
    max_pp = 16
    move_type = "Grass"
    power = 70
    category = "physical"
    def __init__(self):
        super().__init__()

    def attack(self, user, target):
        super().attack(user, target)

class Knock_Off(Move):
    max_pp = 20
    move_type = "Dark"
    power = 65
    category = "physical"
    def __init__(self):
        super().__init__()

    def attack(self, user, target):
        if target.item:
            self.power = 65 * 1.5
        else:
            self.power = 65

        super().attack(user, target)

class U_Turn(Move):
    max_pp = 30
    move_type = "Bug"
    power = 70
    category = "physical"
    def __init__(self):
        super().__init__()

    def attack(self, user, target):
        super().__attack__(user, target)

if __name__ == "__main__":
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

