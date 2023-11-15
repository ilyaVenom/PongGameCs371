# =================================================================================================
# Contributing Authors:	    <Ilya Segal> <Austin Purvis>
# Email Addresses:          <iyse222@uky.edu> <atpu225@uky.edu>
# Date:                     <11/14/23>
# Purpose:                  <The server the manages the clients, and it 
#                           it tell them the playerSide ( Left or Right ), and size of the game>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================
import logging
import time
import socket
import threading

# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

def handleClient(mySocket, otherSocket): # client socket and client num
    
    gameState = mySocket.recv(1024).decode()
    print(gameState)


    syncInfo = mySocket.recv(1024).decode()
    print(syncInfo)

    otherSocket.send(gameState.encode())
    otherSocket.send(syncInfo.encode())
  


players = 0

screenWidth = "700"
screenHeight = "600"
addressList = []


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


    #gameState1 = ""
    #gameState2 = ""

    #t1 = threading.Thread(target=threadFunction, args=(ClientSocket1, 1))
    #t2 = threading.Thread(target=threadFunction, args=(ClientSocket2, 2))
    #t1.start()
    #t2.start()



clientOneStartup = f"{screenWidth} {screenHeight} left"
clientTwoStartup = f"{screenWidth} {screenHeight} right"
print(clientOneStartup)
print(clientTwoStartup)

ClientSocket1.send(clientOneStartup.encode())
ClientSocket2.send(clientTwoStartup.encode())

t1 = threading.Thread(target=handleClient, args=(ClientSocket1, ClientSocket2))
t2 = threading.Thread(target=handleClient, args=(ClientSocket2, ClientSocket1))
t1.start()
t2.start()

ClientSocket1.close()
ClientSocket2.close()
server.close()