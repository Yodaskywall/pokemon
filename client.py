from pokemon import Pokemon, get_natures
from moves import *
from network import Network

def print_info(battle, clientId):
    otherId = (clientId - 1) * -1
    user = battle.teams[clientId][0]
    target = battle.teams[otherId][0]
    print("--------ENEMY-----------")
    print(f"{target.name} ({target.type})")
    print(f"HP: {target.hp}")

    print("\n\n---------USER--------")
    print(f"{user.name} ({user.type})")
    print(f"(HP: {user.hp})")
    print("Moves:")
    for move in user.moves:
        print(move)
    print("\n"*3)
    

def main():
    rillaboom = Pokemon("Rillaboom", [100,125,90,60,70,85], ["Grass"])
    rillaboom.change_nature("Adamant")
    rillaboom.set_evs([252, 56, 0, 0, 60, 140])
    rillaboom.moves = [Fake_Out(), Grassy_Slide(), Knock_Off(), U_Turn()]

    n = Network()
    print("Connected to the server")

    clientId = n.connect()
    print(clientId)
    print("a")
    print("Received connection, client Id is: " + str(clientId))
    team = [rillaboom]
    battle = n.communicate(team)

    while True:
        
        validated = False
        while not validated:
            move = input("Please chose a move (1-4): ")
            if move in [str(x) for x in range(4)]:
                validated = True
                move = int(move)

        battle = n.communicate(move-1)
        battle = n.pickle_receive()
        poke = battle.teams[clientId][0]
        print_info(battle, clientId)


if __name__ == "__main__":
    main()
