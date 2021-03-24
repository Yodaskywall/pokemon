from bs4 import BeautifulSoup
import requests

source = requests.get("https://bulbapedia.bulbagarden.net/wiki/List_of_moves").text
soup = BeautifulSoup(source, "lxml")

tables = soup.find_all("table")
for t in tables:
    if "Pound" in t.text:
        table = t

rows = table.find_all("tr")
moves = []

interest_cols = [1,2,3,5,6]

c = 0
for row in rows:
    c+=1
    if c > 1:
        move = ""
        cols = row.find_all("td")
        for n in interest_cols:
            move += cols[n].text.strip("\n").strip(" ").strip("*") + ","
        accuracy = cols[7].text.strip("\n").strip(" ").strip("*")[:-1]
        try:
            a = int(accuracy)
        except:
            accuracy = 100000
        move += str(accuracy)
        if "Status" not in cols[3].text and "—" not in cols[6].text:
            moves.append(move)

with open("moves.txt", "w") as file:
    for line in moves:
        file.write(line+"\n")
