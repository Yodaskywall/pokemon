import math
import pickle
stat_names = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]

def get_natures():
    with open("natures", "rb") as file:
        natures = pickle.load(file)
    return natures


class Pokemon:
    def __init__(self, name, base_stats, types):
        self.name = name
        self.stats = {}

        i = 0
        self.base_stats = base_stats

        self.type = types

        self.protected = False
        self.protected_last_turn = False
        self.nature = "Serious"
        self.level = 100
        self.moves = [None, None, None, None]
        self.item = None
        self.evs = [0 for x in range(6)]
        self.ivs = [31 for x in range(6)]
        self.calculate_stats()
        self.first_turn = True

    def dead(self):
        if self.hp <= 0:
            return True
        return False

    def calculate_stats(self):
        #HP = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + Level + 10
        #Other Stats = floor(0.01 x (2 x Base + IV + floor(0.25 x EV)) x Level) + 5) x Nature

        natures = get_natures()
        stats = [0 for x in range(6)]
        stats[0] = math.floor(0.01 * (2 * self.base_stats[0] + self.ivs[0] + math.floor(0.25 * self.evs[0])) * self.level) + self.level + 10
        i = 1
        while i < 6:
            stats[i] = math.floor(((0.01 * (2 * self.base_stats[i] + self.ivs[i] + math.floor(0.25 * self.evs[i])) * self.level) + 5) * natures[self.nature][i])
            i += 1

        self.stats = stats
        self.hp = self.stats[0]

    def set_evs(self, evs):
        self.evs = evs
        self.calculate_stats()

    def change_nature(self, nature):
        self.nature = nature
        self.calculate_stats()

    def set_ivs(self, ivs):
        self.ivs = ivs

    def __str__(self):
        return str(self.name) + "\n" + str(self.stats)

def get_pokemon(name):
    pass

