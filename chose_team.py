import pickle
from pokemon import Pokemon, get_natures
from moves import Move, CUSTOM_MOVES

def get_moves():
    moves = []
    for i in range(4):
        custom_move = False
        validated = False
        info = 0
        while not validated:
            validated = True
            move_name = input(f"Please enter the name of move {i + 1}: ")
            with open("moves.txt", "r") as file:
                lines = file.read().split("\n")
            for line in lines:
                line = line.split(",")
                if line[0].upper() == move_name.upper():
                    info = line

            if info == 0:
                if move_name.lower().capitalize() in CUSTOM_MOVES:
                    move = CUSTOM_MOVES[move_name.lower().capitalize()]
                    custom_move = True
                else:
                    print("Invalid move, please try again")
                    validated = False

        if not custom_move:
            move = Move()
            move.name = info[0]
            move.move_type = info[1]
            move.category = info[2]
            move.max_pp = int(int(info[3]) * 1.6)
            move.power = int(info[4])
            move.accuracy = int(info[5])
        moves.append(move)
    return moves


def get_pokemon():
    validated = False
    while not validated:
        validated = True
        name = input("Please enter the name of your pokemon: ")
        with open("pokemon_info", "r") as file:
            lines = file.read().split("\n")

        info = 0
        for line in lines:
            line = line.split(",")
            if line[0].upper() == name.upper():
                info = line
        
        if info == 0:
            print("Pokemon not found, please try again.")
            validated = False

    name = info[0]
    types = [info[1], info[2]]
    if types[1] == "None":
        types = [types[0]]
    stats = [int(info[x]) for x in range(3, len(info))]
    print(stats)
    pokemon = Pokemon(name, stats, types)
    pokemon.moves = get_moves()

    pokemon.change_nature("Adamant")
    pokemon.set_evs([252, 56, 0, 0, 60, 140])
    return pokemon

def get_pokemon_file(name):
    with open("pokemon_info", "r") as file:
        lines = file.read().split("\n")

    info = 0
    for line in lines:
        line = line.split(",")
        if line[0].upper() == name.upper():
            info = line
        
    if info == 0:
        print("Pokemon not found, please try again.")

    else:
        name = info[0]
        types = [info[1], info[2]]
        if types[1] == "None":
            types = [types[0]]
        stats = [int(info[x]) for x in range(3, len(info))]
        pokemon = Pokemon(name, stats, types)

        return pokemon

def get_moves_file(move_list):
    print(move_list)
    moves = []
    for i in range(4):
        custom_move = False
        validated = False
        info = 0
        move_name = move_list[i]
        with open("moves.txt", "r") as file:
            lines = file.read().split("\n")
        for line in lines:
            line = line.split(",")
            if line[0].upper() == move_name.upper():
                info = line

        if info == 0:
                if move_name.lower().capitalize() in CUSTOM_MOVES:
                    move = CUSTOM_MOVES[move_name.lower().capitalize()]
                    custom_move = True
                else:
                    print(f"{move_name} is an Invalid move, please try again")
                    validated = False

        if not custom_move:
            move = Move()
            move.name = info[0]
            move.move_type = info[1]
            move.category = info[2]
            move.max_pp = int(int(info[3]) * 1.6)
            move.power = int(info[4])
            move.accuracy = int(info[5])
        moves.append(move)
    return moves
