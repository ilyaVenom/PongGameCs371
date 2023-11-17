# =================================================================================================
# Contributing Authors:	    <Ilya Segal> <Austin Purvis>
# Email Addresses:          <iyse222@uky.edu> <atpu225@uky.edu>
# Date:                     <11/14/23>
# Purpose:                  <The server the manages the clients, and it 
#                           it tell them the playerSide ( Left or Right ), and size of the game>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================
import socket
import threading
import json

gameState1 = {
    "playerPaddle": [],
    "opponentPaddle": [],
    "ball": [],
    "lscore": 0,
    "rscore": 0,
    "sync": 0
}

gameState2 = {
    "playerPaddle": [],
    "opponentPaddle": [],
    "ball": [],
    "lscore": 0,
    "rscore": 0,
    "sync": 0
}

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

def handleClient(mySocket:socket.socket, number:int): # client socket and client num
    gameDataDict = {}
    global gameState1
    global gameState2

    try:
        while True:
            gameData = mySocket.recv(1024).decode()
            if gameData:
                gameDataDict = json.loads(gameData)
            
            gameDataDict = json.loads(gameData)

            if number == 1:
                gameState1 = gameDataDict
            else:
                gameState2 = gameDataDict

            gameState1["opponentPaddle"] = gameState2["playerPaddle"]
            gameState2["opponentPaddle"] = gameState1["playerPaddle"]

            if gameState1["sync"] > gameState2["sync"]:
                if number == 1:
                    mySocket.send(json.dumps(gameState1).encode())
                else:
                    gameState1["playerPaddle"], gameState1["opponentPaddle"] = gameState1["opponentPaddle"], gameState1["playerPaddle"]
                    mySocket.send(json.dumps(gameState1).encode())
            else:
                if number == 2:
                    mySocket.send(json.dumps(gameState2).encode())
                else:
                    gameState2["playerPaddle"], gameState2["opponentPaddle"] = gameState2["opponentPaddle"], gameState2["playerPaddle"]
                    mySocket.send(json.dumps(gameState2).encode())

    except Exception as e:
        print(f"Error handling client {number}: {e}")
    finally:
        mySocket.close()
   
  


players = 0
screenWidth = "700"
screenHeight = "600"
addressList = []
lscore = 0
rscore = 0


# Creating the server's socket and binding it to an IP + Port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server
server.bind(("localhost",1234))


while (players < 2):
    print("Server listening...")
    server.listen(5)

    # Client 1
    ClientSocket1, address = server.accept()
    addressList.append(address)
    print(f"Connect from {address} has been made.")
    players += 1
    ClientSocket1.send("waiting".encode())

    # Client 2
    ClientSocket2, address = server.accept()
    addressList.append(address)
    print(f"Connect from {address} has been made.")
    players += 1



clientOneStartup = f"{screenWidth} {screenHeight} left"
clientTwoStartup = f"{screenWidth} {screenHeight} right"
print(clientOneStartup)
print(clientTwoStartup)

ClientSocket1.send(clientOneStartup.encode())
ClientSocket2.send(clientTwoStartup.encode())

t1 = threading.Thread(target=handleClient, args=(ClientSocket1, 1))
t2 = threading.Thread(target=handleClient, args=(ClientSocket2, 2))
t1.start()
t2.start()

while True:
    client1game = {}
    client2game = {}

    client1str = ClientSocket1.recv(1024).decode()
    if client1str:
        client1game = json.loads(client1str)

    client2str = ClientSocket2.recv(1024).decode()
    if client2str:
        client2game = json.loads(client2str)

    if client1game["sync"] > client2game["sync"]:
        ClientSocket1.send(json.dumps(client1game["sync"]).encode())
        ClientSocket2.send(json.dumps(client1game["sync"]).encode())
    else:
        ClientSocket1.send(json.dumps(client2game["sync"]).encode())
        ClientSocket2.send(json.dumps(client2game["sync"]).encode())

    if client1game["lscore"] == 5 | client1game["rscore"] == 5 | client2game["lscore"] == 5 | client2game["rscore"] == 5:
        break


ClientSocket1.close()
ClientSocket2.close()
server.close()