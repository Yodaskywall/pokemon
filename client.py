from pokemon import Pokemon, get_natures
from moves import *
from network import Network
from chose_team import *
from read_team import read_team
import pickle

def print_info(battle, clientId):
    otherId = (clientId - 1) * -1
    user = battle.teams[clientId][battle.current_pokemon[clientId]]
    target = battle.teams[otherId][battle.current_pokemon[otherId]]
    print("--------ENEMY-----------")
    print(f"{target.name} ({target.type})")
    print(target.hp)
    print(target.stats[0])
    print(f"HP: {target.hp} ({str(target.hp * 100/target.stats[0])[:6]}%)")

    print("\n\n---------USER--------")
    print(f"{user.name} ({user.type})")
    print(f"HP: {user.hp} ({str(user.hp * 100/user.stats[0])[:6]}%)")
    print("Moves:")
    for move in user.moves:
        print(move.name)
    print("\n"*3)
    

def print_enemy_team(battle, clientId):
    print("Enemy team: ")
    for pokemon in battle.teams[abs(clientId - 1)]:
        print(pokemon.name)

    print("\nYour team: ")
    for pokemon in battle.teams[clientId]:
        print(pokemon.name)
        print()


def main():

    n = Network()
    print("Connected to the server")

    clientId = n.connect()
    print(clientId)
    print("a")
    print("Received connection, client Id is: " + str(clientId))
    filename = input("Please enter the name of the file where the team is stored: ")
    team = read_team(filename)
    battle = n.communicate(team)

    started = False

    while True:
        if not started:
            print("Searching for oppent..")
            opponent_id = abs(clientId - 1)
            if battle.teams[opponent_id] is None:
                battle = n.pickle_receive()
            print("Opponent found")
            print_enemy_team(battle, clientId)

            validated = False
            while not validated:

                

                ans = input("What pokemon do you want to start with (1-6)?: ")
                if ans not in [str(x) for x in range(1,7)]:
                    print("Invalid input please try again")
                else:
                    validated = True
                    current_pokemon = int(ans) - 1

            battle = n.communicate(current_pokemon)
            started = True
            
        if battle.get_pokemon(clientId).dead():
            validated = False
            while not validated:
                change_to = input("Your pokemon is dead. What will you change to (1-6): ")
                if change_to in [str(x) for x in range(1,7)]:
                    change_to = int(change_to) - 1
                    if battle.teams[clientId][change_to].dead() or battle.current_pokemon[clientId] == change_to:
                        print("You cannot change to that pokemon. Please try again")
                    else:
                        validated = True

                else:
                    print("Invalid input please try again.")
            n.pickle_send(change_to)

        validated = False
        while not validated:
            print_info(battle, clientId)
            move = input("Please chose a move (1-4) or change pokemon (5): ")
            if move in [str(x) for x in range(1,6)]:
                validated = True
                move = int(move)
            else:
                print("Invalid move please try again")

        if move == 5:
            validated = False
            while not validated:
                change_to = input("Please enter the pokemon you want to change to (1-6): ")
                if change_to in [str(x) for x in range(1,7)]:
                    change_to = int(change_to)
                    if battle.current_pokemon[clientId] != (change_to-1):
                        validated = True
                        move += change_to

                    else:
                        print("That pokemon is already on the field")

                else:
                    print("Invalid input, please try again")

        battle = n.communicate(move-1)
        battle = n.pickle_receive()
        poke = battle.teams[clientId][0]


if __name__ == "__main__":
    main()
