import socket
from _thread import start_new_thread
import pygame
from battle import Battle
from network import *
from random import randint

HEADERSIZE = 10

server = "192.168.43.108"
#server = "169.254.58.247"
port = 25565

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)

s.listen()
print("Waiting for a connection, Server Started.")

battles = {
    0 : Battle(0)
}

conns = {
    0 : [None, None]
}

def main_loop(battleId):
    while True:
        battle = battles[battleId]
        if battle.move_ready():
            print("do calculation")
            print(f"Move 0: {battle.moves[0]}") 
            print(f"Move 1: {battle.moves[1]}") 
            if battle.moves[0] in range(6):
                battle.current_pokemon[0] = battle.moves[0]
                pokemon = [battle.teams[0][battle.current_pokemon[0]], battle.teams[1][battle.current_pokemon[1]]]
                battle.moves[1].attack(pokemon[1], pokemon[0])
            
            elif battle.moves[1] in range(6):
                battle.current_pokemon[1] = battle.moves[1]
                pokemon = [battle.teams[0][battle.current_pokemon[0]], battle.teams[1][battle.current_pokemon[1]]]
                battle.moves[0].attack(pokemon[0], pokemon[1])

            else:
                pokemon = [battle.teams[0][battle.current_pokemon[0]], battle.teams[1][battle.current_pokemon[1]]]
                priorities = [0,0]
                priorities[0] = battle.moves[0].priority
                priorities[1] = battle.moves[1].priority
                
                if priorities[0] == priorities[1]:
                    if pokemon[0].stats[5] > pokemon[1].stats[5]:
                        first = 0
                    elif pokemon[0].stats[5] < pokemon[1].stats[5]:
                        first = 1

                    else:
                        first = randint(0,1)

                elif priorities[0] > priorities[1]:
                    first = 0
                
                else:
                    first = 1

                last = (first - 1) * - 1
                battle.moves[first].attack(pokemon[first], pokemon[last])
                print(f"{pokemon[first].name} usedd {battle.moves[first].name}")
                print(pokemon[first].protected)
                print(pokemon[last].protected)
                battle.moves[last].attack(pokemon[last], pokemon[first])
                print(f"{pokemon[last].name} used {battle.moves[last].name}")
                

            battle.moved = [False, False]
            battle.moves = [None, None]
            battles[battleId] = battle
            pickle_send(conns[battleId][0], battle)
            pickle_send(conns[battleId][1], battle)
            for poke in pokemon:
                if poke.protected:
                    poke.protected = False
                    poke.protected_last_turn = True

                else:
                    poke.protected_last_turn = False
                
                

            

def threaded_client(conn, clientId, battleId):
    battles[battleId].connected[clientId] = True
    conns[battleId][clientId] = conn
    battle = battles[battleId]
    print(f"Sending {clientId} to client.")
    pickle_send(conn, clientId)
    team = pickle_receive(conn)
    battle = battles[battleId]
    battle.teams[clientId] = team
    battles[battleId] = battle
    pickle_send(conn, battle)
    opponent_id = abs(clientId - 1)
    opponent_connected = True
    if battle.teams[opponent_id] is None:
        opponent_connected = False
    connected = True
    opponent_chose_lead = False

    while connected:
        if (not opponent_connected) and battles[battleId].teams[opponent_id]:
            pickle_send(conn, battle)
            opponent_connected = True
        
        elif opponent_connected and battles[battleId].current_pokemon[clientId] == -1:
            pokeI = pickle_receive(conn)
            battle = battles[battleId]
            battle.current_pokemon[clientId] = pokeI
            if battles[battleId].current_pokemon[opponent_id] != -1:
                opponent_chose_lead = True
                pickle_send(conn, battle)
            battles[battleId] = battle

        elif (not opponent_chose_lead) and battles[battleId].current_pokemon[opponent_id] != -1:
            print("YOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
            pickle_send(conn, battles[battleId])
            opponent_chose_lead = True


        elif opponent_connected and opponent_chose_lead:
            if not battle.moved[clientId]:
                print(f"f en el chat para el cliente {clientId}")
                if battle.get_pokemon(clientId).dead():
                    change_to = pickle_receive(conn)
                    battle = battles[battleId]
                    battle.current_pokemon[clientId] = change_to
                move = pickle_receive(conn)
                battle = battles[battleId]
                if move > 4:
                    battle.moves[clientId] = move - 4
                else:
                    battle.moves[clientId] = battle.get_pokemon(clientId).moves[move]
                battle.moved[clientId] = True
                battles[battleId] = battle
                pickle_send(conn, battle)

            elif not battle.move_ready():
                # Waiting for opponent
                pass
            


battleId = 0
clientId = 0

while True:
    conn, address = s.accept()
    print(f"Connected to {address}.")

    start_new_thread(threaded_client, (conn, clientId, battleId))
    print(f"Player {clientId} connected to server {battleId}")
    if clientId == 0:
        start_new_thread(main_loop, (battleId,))

    clientId += 1

    if clientId == 2:
        print("New Game Created")
        clientId = 0
        battleId += 1
        battles[battleId] = Battle(battleId)
        conns[battleId] = [None, None]
