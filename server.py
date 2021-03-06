import socket
from _thread import start_new_thread
import pygame
from battle import Battle
from network import *
from random import randint

HEADERSIZE = 10

server = "192.168.43.108"
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
            pokemon = [battle.teams[0][0], battle.teams[1][0]]
            if pokemon[0].stats[5] > pokemon[1].stats[5]:
                first = 0
            elif pokemon[0].stats[5] < pokemon[1].stats[5]:
                first = 1

            else:
                first = randint(0,1)
            last = (first - 1) * - 1
            battle.moves[first].attack(pokemon[first], pokemon[last])
            battle.moves[last].attack(pokemon[last], pokemon[first])
            battle.moved = [False, False]
            battle.moves = [None, None]
            battles[battleId] = battle
            pickle_send(conns[battleId][0], battle)
            pickle_send(conns[battleId][1], battle)
            
            

            

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

    connected = True

    while connected:
        if not battle.moved[clientId]:
            move = pickle_receive(conn)
            battle = battles[battleId]
            battle.moves[clientId] = battle.teams[clientId][0].moves[move]
            battle.moved[clientId] = True
            battles[battleId] = battle
            pickle_send(conn, battle)

        elif not battle.move_ready():
            print("Waiting for opponent")
            
        


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
