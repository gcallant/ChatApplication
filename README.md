# Rock Paper Scissors Application

1)	In this game you will be playing the game rock, paper, scissors against one other person by starting up a client program, which then calls to a server for a connection.  The server then connects you to another player from a queue and then you play until one person wins.

2)	The game will be operated by four major pieces:
•	Server
•	Client
•	Client Management
•	Queue

3)	Protocol: 
The game will start off by having the server up and running waiting for a request to join the game.  Once a request comes in the server will send out a message telling the player welcome to the game.  If there is an open slot in the game he will be added to the playable game.  If he is the first player in the server will display a message saying that it is searching for another player.  If he is the second player he will be added to the game with the first.  Any other new players will be added to a queue and will be added to the game once a slot becomes available.

4)	Document Usage:
This game uses a client-server system in order to operate and play.  In order for the game to function properly, the server should be started before any of the clients try to connect.

Server Program:
In order to launch the server program, you must first run the server program provided.  In order to get the server up and running, you must open up the command prompt of whichever operating system you are using and locate the server program within your computer.  Once you have located the file you can run it by typing “python server.py”.  At this point the server is then up and running and waiting to make connections.


Client Program:
In order to launch the game one must first run the client code provided.  To start the program you would open up the command prompt of whichever operating system you are running and find your way to where the client program is saved.  Once you have found it run the command “python client.py”.  The program will start to run and it will make request to the server program.  If it is running the client program will receive a notification from it saying that you have either been placed into a game and it will start soon if someone else is in the game as well, or the server will put you into a queue of people waiting to play the game.

5)	Specifications:
Here are a few notes/specs about this program:
•	The computer needs to be running Python 2.7
•	Operating system needs to be Linux (for now…)
•	At least one computer is needed that can run and host the server program
•	The server can host up to two players in the game and six people waiting to play in the queue
•	The game will play the best of three games to determine a winner
•	If someone disconnects early and they were in the current game a new player will be pulled from the queue and the scores will be reset.
•	Once a game is finished the players will be given the option to play again or to quit the game.  If they decide to play again, they will be placed into the queue and will have to wait there turn to play again.  If they choose to quit then their connection to the server will be closed.

•	Test Cases:
Here is a list of what we tried in order to break our program.
