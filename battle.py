class Battle:
    def __init__(self, battleId):
        self.id = battleId
        self.teams = [None, None]
        self.connected = [False, False]
        self.lost = [False, False]
        self.current_pokemon = [-1, -1]
        self.moved = [False, False]
        self.moves = [None, None]

    def move_ready(self):
        return self.moved[0] and self.moved[1]

    def isready(self):
        return self.connected[0] and self.connected[1]

    def finished(self):
        return self.lost[0] or self.lost[1]

    def get_pokemon(self, clientId):
        return self.teams[clientId][self.current_pokemon[clientId]]
