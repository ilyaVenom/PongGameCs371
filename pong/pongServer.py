# =================================================================================================
# Contributing Authors:	    <Ilya Segal> <Austin Purvis>
# Email Addresses:          <iyse222@uky.edu> <atpu225@uky.edu>
# Date:                     <11/17/23>
# Purpose:                  <The server the manages the clients, and it synchronizes the two based
#                            on sync values. Game states are exchanged based on sync.>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================
import socket
import threading
import json

# Values for the game's current state
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

# Author:   Austin Purvis <atpu225@uky.edu>
# Purpose:  This method should allow the two client threads to exchange their information with the server and receive the most up to date info in return.
# Pre:      Two threads should be created and passed to this method. gameStates should be initialized as above. The clients should be starting their games.
# Post:     Global varaibles gameState1 and gameState2 will be updated based on what the clients send.

def handleClient(mySocket:socket.socket, number:int): # client socket and client num
    
    # Empty dictionary to handle incoming data
    gameDataDict = {}
    global gameState1
    global gameState2

    #try:
    while True:
        # Receiving data from client
        gameData = mySocket.recv(1024).decode()
        # if gameData:
        #     gameDataDict = json.loads(gameData)
        
        # Converting string from client into dictionary via json library
        gameDataDict = json.loads(gameData)

        # Setting global variable based on which client thread is running (1 or 2)
        # Setting opponent to be the opposite number
        # THIS IS WHERE OUR ISSUE IS
        if number == 1:
            gameState1 = gameDataDict
            gameState1["opponentPaddle"] = gameState2["playerPaddle"]

        else:
            gameState2 = gameDataDict
            gameState2["opponentPaddle"] = gameState1["playerPaddle"]
            

        # Determining which game state is ahead and conforming to it by sending its game state back to both clients
        if gameState1["sync"] > gameState2["sync"]:
            if number == 1:
                mySocket.send(json.dumps(gameState1).encode())
            else:
                # If 1 is ahead, use 1's data but swap player and opponent to send to 2 (So 2 doesnt view 1's data as its own)
                gameState1["playerPaddle"], gameState1["opponentPaddle"] = gameState1["opponentPaddle"], gameState1["playerPaddle"]
                mySocket.send(json.dumps(gameState1).encode())
        else:
            # Same case as above but with 2 being ahead
            if number == 2:
                mySocket.send(json.dumps(gameState2).encode())
            else:
                gameState2["playerPaddle"], gameState2["opponentPaddle"] = gameState2["opponentPaddle"], gameState2["playerPaddle"]
                mySocket.send(json.dumps(gameState2).encode())

    # except Exception as e:
    #     print(f"Error handling client {number}: {e}")
    # finally:
    #     mySocket.close()
   
  

# Initialization variables
players = 0
screenWidth = "700"
screenHeight = "600"
lscore = 0
rscore = 0


# Creating the server's socket and binding it to an IP + Port
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server
server.bind(("localhost",1234))

# While the number of connected clients is less than 2 (players)
while (players < 2):
    print("Server listening...")
    server.listen(5) # Listen for incoming connections

    # Client 1
    ClientSocket1, address = server.accept() # accepting a connection
    print(f"Connect from {address} has been made.")
    players += 1
    ClientSocket1.send("waiting".encode()) # Tell the first client to display a wait message

    # Client 2
    ClientSocket2, address = server.accept() # Accept second connection
    print(f"Connect from {address} has been made.")
    players += 1


# Send the startup message to both clients (screen width, height, playerSide)
clientOneStartup = f"{screenWidth} {screenHeight} left"
clientTwoStartup = f"{screenWidth} {screenHeight} right"
print(clientOneStartup)
print(clientTwoStartup)

ClientSocket1.send(clientOneStartup.encode())
ClientSocket2.send(clientTwoStartup.encode())

# Thread both client connection to the handleClient method
t1 = threading.Thread(target=handleClient, args=(ClientSocket1, 1))
t2 = threading.Thread(target=handleClient, args=(ClientSocket2, 2))
t1.start()
t2.start()

# Loop to update sync value
while True:

    # Empty dictonaries for game states
    client1game = {}
    client2game = {}

    # Receive json dump string
    client1str = ClientSocket1.recv(1024).decode()
    
    # Load it into dictionary
    if client1str:
        client1game = json.loads(client1str)

    # Same process as above
    client2str = ClientSocket2.recv(1024).decode()
    if client2str:
        client2game = json.loads(client2str)

    # Compare sync values, whichever is larger is sent to client's to be updated
    if client1game["sync"] > client2game["sync"]:
        ClientSocket1.send(json.dumps(client1game["sync"]).encode())
        ClientSocket2.send(json.dumps(client1game["sync"]).encode())
    else:
        ClientSocket1.send(json.dumps(client2game["sync"]).encode())
        ClientSocket2.send(json.dumps(client2game["sync"]).encode())

    # check if either score is 5. If so, end loop
    if client1game["lscore"] == 5 | client1game["rscore"] == 5 | client2game["lscore"] == 5 | client2game["rscore"] == 5:
        break

# Closing connection sockets
ClientSocket1.close()
ClientSocket2.close()
server.close()