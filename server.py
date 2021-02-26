import socket
from _thread import start_new_thread
import pygame

HEADERSIZE = 10

server = "192.168.1.108"
port = 25565

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)

s.listen()
print("Waiting for a connection, Server Started.")

battles = {

}

def main_loop(gameId):
    pass


gameId = 0
clientId = 0

while True:
    conn, address = s.accept()
    print(f"Connected to {address}.")

    start_new_thread(threaded_client, (conn, clientId, gameId))
    print(f"Player {clientId} connected to server {gameId}")
    if clientId == 0:
        start_new_thread(main_loop, (gameId,))

    clientId += 1

    if clientId == 2:
        print("New Game Created")
        clientId = 0
        gameId += 1
        games[gameId] = Game(gameId)
