from pokemon import Pokemon
from chose_team import get_pokemon_file, get_moves_file
stat_names = ["HP", "ATK", "DEF", "SPA", "SPD", "SPE"]

def read_team(filename):
    with open(filename, "r") as file:
        lines = file.read().split("\n")
    team = []
    c = 0
    l = 0

    poke_info = []
    team = []

    for line in lines:
        if l == 0:
            if line.split(" ")[0] == "":
                pass
            else:
                moves = []
                name = line.split(" ")[0]
                l += 1
        elif l > 0:
            if "EVs" in line:
                line = line[5:].split("/")
                evs = [0,0,0,0,0,0]
                for ev_st in line:
                    ev_st = ev_st.split(" ")

                    for h in ev_st:
                        if h == "":
                            ev_st.remove(h)

                    stat_index = stat_names.index(ev_st[1].strip(" ").upper())
                    evs[stat_index] = int(ev_st[0].strip(" "))
            elif "Nature" in line:
                line = line.split(" ")
                nature = line[0]

            elif len(line) > 1 and line[0] == "-":
                move = line[2:].strip(" ")
                moves.append(move)
                if len(moves) == 4:
                    l = 0
                    poke = get_pokemon_file(name)
                    poke.moves = get_moves_file(moves)
                    poke.set_evs(evs)
                    poke.change_nature(nature)
                    team.append(poke)

        elif line.strip(" ").strip("\t") == "":
            c+=1
    
    if __name__ == "__main__":
        for pokemon in team:
            print(pokemon.name)
            print(pokemon.evs)
            for move in pokemon.moves:
                print(move)
            print(pokemon.nature)
            print("***************")

    return team  
    #name = info[0]
    #types = [info[1], info[2]]
    #if types[1] == "None":
    #    types = [types[0]]
    #stats = [int(info[x]) for x in range(3, len(info))]
    #print(stats)
    #pokemon = Pokemon(name, stats, types)
    #pokemon.moves = get_moves()

    #pokemon.change_nature("Adamant")
    #pokemon.set_evs([252, 56, 0, 0, 60, 140])
 

if __name__ == "__main__":
    read_team("team1.txt")
