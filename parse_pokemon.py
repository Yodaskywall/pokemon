from bs4 import BeautifulSoup
import requests
import pickle

file = open("type_info", "rb")
types = pickle.load(file)[0]
file.close()


source = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_Pok%C3%A9mon_by_National_Pok%C3%A9dex_number").text
soup = BeautifulSoup(source, "lxml")
table = soup.find_all("table")[1]
tr = table.find_all("tr")

pokemon = []
pokemon_stats = {}
lines = []

for row in tr:
    try:
        poke = row.find_all("td")[2].text.strip("\n")
        if poke not in pokemon:
            pokemon.append(poke)
    except:
        pass

counter = 0
for poke in pokemon:
    counter += 1
    print(counter)
    source = requests.get(f"https://bulbapedia.bulbagarden.net/wiki/{poke}").text
    soup = BeautifulSoup(source, "lxml")
    tables = soup.find_all("table")
    table = 0
    for t in tables:
        if "At Lv. 50" in t.text:
            table = t
            break
    if table != 0:
        pokemon_stats[poke] = []
        rows = table.find_all("tr")
        for i in range(2, len(rows)-2):
            th = rows[i].find_all("th")[0].text
            stat = ""
            found = False
            for c in th:
                if found:
                    stat += c
                if c == ":":
                    found = True
            pokemon_stats[poke].append(int(stat))


    type_table = 0
    for x in soup.find_all("table"):
        if "Abilities" in x.text:
            type_table = x
            break
    table = type_table
    if table != 0:
        rows = table.find_all("tr")
        for row in rows:
            if "Type" in row.text:
                tipe_unprocessed = row.text.split("\n")
                tipe = []
                for t in tipe_unprocessed:
                    if t.strip(" ") in types:
                        tipe.append(t.strip(" "))

                if len(tipe) > 2:
                    tipe = tipe[:2]
                if len(tipe) == 1:
                    tipe.append("None")

    line = f"{poke.strip(' ')},{tipe[0]},{tipe[1]}"
    for stat in pokemon_stats[poke]:
        line += "," + str(stat)
    lines.append(line)

with open("pokemon_info", "w") as file:
    for line in lines:
        try:
            file.write(line + "\n")
        except:
            pass
    

