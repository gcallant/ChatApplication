# Rock Paper Scissors Application

1)	In this game you will be playing the game rock, paper, scissors 
against one other person by starting up a client program, which then 
calls to a server for a connection.  The server then connects you to 
another player from a queue and then you play until one person wins.

2)	The game will be operated by four major pieces:
* Server
*	Client
*	Client Management
*	Queue

3)	Protocol: 
The game will start off by first starting the server.  The server creates
a new ServerSocket on localhost, on a specified port number, and blocks,
waiting to accept a connection on that port.  Once a request comes in the
server will create a new client socket for that connection, and will send
out a message telling the player welcome to the game.  If there is an open
slot in the game the player will be added to the playable game.  If the
player is the first player to connect, the server will display a message 
saying that it is searching for another player.  If the player to connect
is the second player, this player will be added to the game with along with
the first player.  Any other new players will be added to a queue and will
be added to the game once a slot becomes available.

4)	Document Usage:
This game uses a client-server system in order to operate and play.  In order
for the game to function properly, the server should be started before any of
the clients try to connect.

Assumptions: You must have Python 2.7 or greater installed on your operating
system in order to use the functionality provided by this program. Visit 
[this link](https://www.python.org/downloads/) to download a version of Python
for your operating system.

Server Program:
In order to launch the server program, you must first run the server program
provided.  In order to get the server up and running, you must either open up a
command prompt or terminal in whichever operating system you are using and locate
the server program within your computer.  Once you have located the file you can
run it by typing “python server.py <IP Address> <Port #> <Max Queue Size> <Buffersize>”
and you will pass it four parameters. Those parameters are passed in using a required
order, which is <IP Address>, <Port #>, <Max Queue Size>, and <Buffersize>.  The first
two parameters are required, while the second two are variables that you can use to
modify the game.  After this point, the server is then up and running and waiting to
accept incoming connections.


Client Program:
In order to launch the game you must either open up a command prompt or terminal in
whichever operating system you are using and locate the client program within your
computer.  Once you have located the file you can run it by typing “python client.py <IP Address> <Port #>”
and you will pass it two required parameters. Those parameters are passed in using a
required order, which is <IP Address> and <Port #>.  If the server is running the
client program will receive a notification from it saying that you have either been
placed into a game and it will start soon if someone else is in the game as well, or
the server will put you into a queue of people waiting to play the game.

5)	Specifications:
Here are a few notes/specs about this program:
*	The computer needs to be running at least Python 2.7 or greater.
*	Operating system has to support Python.
*	At least one computer is needed that can run and host the server program
*	The server can host up to two players in the game and six people waiting to play in the queue
*	The game will play the best of three games to determine a winner
*	If someone disconnects early and they were in the current game a new player will be pulled
  from the queue and the scores will be reset.
*	Once a game is finished the players will be given the option to play again or to quit the game.
  If they decide to play again, they will be placed into the queue and will have to wait their 
  turn to play again.  If they choose to quit then their connection to the server will be closed.

Test Cases:
Here is a list of smoke testing we have attempted.
*	We have tried using command + c while in a client to end the connection abruptly and see if a
  player would be added to a game from the queue.
*	Test handling of server disconnect.
*	Test handling of clients when queue is full.
*	Test handling of when the queue is full and the current game ends, player is added to game from queue
*	Tested what happens when the queue is full and someone tries to join.
