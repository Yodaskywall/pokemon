import pickle

stats = ["HP", "Attack", "Defense", "Sp. Attack", "Sp. Defense", "Speed"]
natures = {}


with open("natures.txt", "r") as file:
    lines = file.read().split("\n")
    for line in lines:
        print(line.split("\t"))
        line = line.split("\t")
        if line[3] not in stats:
            natures[line[1]] = [1 for x in range(6)]

        else:
            nature = [1 for x in range(6)]
            nature[stats.index(line[3])] = 1.1
            nature[stats.index(line[4])] = 0.9
            natures[line[1]] = nature

for nature in natures:
    print(nature, natures[nature])

with open("natures", "wb") as file:
    pickle.dump(natures, file)

