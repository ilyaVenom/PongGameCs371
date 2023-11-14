# =================================================================================================
# Contributing Authors:	    <ilya segal>
# Email Addresses:          <iyse222@uky.edu>
# Date:                     <11/14/23>
# Purpose:                  <The server the manages the clients, and it 
#                           it tell them the playerSide ( Left or Right ), and size of the game>
# Misc:                     <Not Required.  Anything else you might want to include>
# =================================================================================================
import logging
import time
import socket
import threading
# num of players:
players = 0
# Use this file to write your server logic
# You will need to support at least two clients
# You will need to keep track of where on the screen (x,y coordinates) each paddle is, the score 
# for each player and where the ball is, and relay that to each client
# I suggest you use the sync variable in pongClient.py to determine how out of sync your two
# clients are and take actions to resync the games

# look over server side sat.
# 1. defined socket:
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)      # Creating the server
# next bind it:

# and the user 
server.bind(("localhost",1234))
# and are we working on the local host?
# next listen:
server.listen(5)


while (players < 2):# might not need the while loop
    #ClientSocket, address = server.accept()
    #print(f"Connect from {address} has been made.")

    # but instead join game
    # and connect to a game.
    #ClientSocket.send(bytes("welcome to the server","utf-8"))

    # and send a list of
    # screenWidth, screenHeight, left or right
    #screenWidth = "700"
    #screenHeight = "600"
    #playerSide = "left"

    #msg = f"{screenWidth}",{screenHeight},{playerSide}
    #ClientSocket.send(msg.encode())

    # Client 1
    ClientSocket1, address = server.accept()
    print(f"Connect from {address} has been made.")

    screenWidth = "700"
    screenHeight = "600"
    playerSide = "left"

    message = f"{screenWidth},{screenHeight},{playerSide}"
    ClientSocket1.send(message.encode())
    

    # Client 2
    ClientSocket2, address = server.accept()
    print(f"Connect from {address} has been made.")

    screenWidth = "700"
    screenHeight = "600"
    playerSide = "right"

    message = f"{screenWidth},{screenHeight},{playerSide}"
    ClientSocket2.send(message.encode())

    gameState1 = ""
    gameState2 = ""

    t1 = threading.Thread(target=threadFunction, args=(ClientSocket1, 1))
    t2 = threading.Thread(target=threadFunction, args=(ClientSocket2, 2))
    t1.start()
    t2.start()

    # implement the thread function:

    # next after building the window,
    # then player position in thread

    # build thread func

    # building the threads - is the next step



#def thread(clientSocket, Cnum1): # client socket and client num
#write thread logic, to accept a game state
# something to hold the gameStates
# for gameState 1 and another for 2.
# test
width = 700

height = 600
# send the width and hieght to the client.

#So, the server is the middle
# And the paddles are the clients. 
server.recv(1024).decode()

ClientSocket.close()
server.close()