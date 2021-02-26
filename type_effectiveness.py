from bs4 import BeautifulSoup
import requests
import pickle

types = []
type_effective = {}

source = requests.get("https://bulbapedia.bulbagarden.net/wiki/Type").text
soup = BeautifulSoup(source, "lxml")
tables = soup.findAll("table")
for table in tables:
    if "Defending type" in table.text:
        break

i = 0
for row in table.findAll("tr"):
    if i == 1:
        for a in row.findAll("a"):
            types.append(a["title"])
    if i > 1:
        tipo = row.findAll("a")[0]["title"]
        if "Generation" not in tipo:
            type_effective[tipo] = []

            for col in row.findAll("td"):
                try:
                    mult = col.text[1]
                    if mult not in [str(x) for x in range(3)]:
                        mult = 0.5
                    mult = float(mult)
                    type_effective[tipo].append(mult)

                except:
                    pass

    i += 1
print(types)
for tipo in type_effective:
    print(tipo)
    print(type_effective[tipo])

type_info = [types, type_effective]

with open("type_info", "wb") as file:
    pickle.dumps(type_info, file)


