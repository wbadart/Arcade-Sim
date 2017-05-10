# Arcade-Sim
Pygame based arcade simulator.

This application is the final project for the Notre Dame CSE class
in programming paradigms. A study in the event-driven paradigm,
*Arcade Sim* leverages the [Pygame](https://www.pygame.org) library
for gameplay and the [Twisted](#) library for multiplayer.

## Team
- Brittany DiGenova -- *bdigenova*
- Will Badart -- *wbadart**

##Github Repo
https://github.com/wbadart/Arcade-Sim

##Download and Beginning Gameplay
If you would like to play a single player game, go to the src directory under Arcade-Sim
and run python3 main.py -p 1 this will set your preferred user settings to single player.
If, however, you would like to join a pre-existing game, run python3 main.py -p 2. This will
connect you to the listening local port on player one's game and begin interactive gameplay.

##User Interface
Upon opening the game you will be presented with an Arcade simulator screen. If you have any
questions press h in order to navigate to the help menu, and press m to return to the main 
screen. Keyboard interrupt (ctrl-c) to leave the game. 

##Key Commands
s - down
a - left
w - up
d - down
j - select A
k - select B

Note that upon pressing the keys the corresponding key will press at the bottom of the arcade
simulator. If you use the s,a,w,d keys they will move the joystick at the bottom left of the 
screen.

##Entering Game
Use s to toggle between games in the arcade, and press j to enter the game of choice.

##Snake
Snake is the game that we fully developed for the sake of this project. The rules are as follows:
- Use the move keys to move your snake around the screen in order to collide with the single "food" square in order to grow and gain points
- Do not collide with your own snake or you will die (for two player mode also cannot collide with the other person's snake)

If you are in multiplayer mode, two snakes of different color will appear on the screen, you must race to eat the food without colliding 
with yourself or the other player. 

##Pacman
We began a prototype for pacman in order to acheive our overall goal of recreating an Arcade feel. We did not finish the gameplay for pacman
as developing gameplay and network interaction for one game proved to be a hefty task. Currently pacman can move anywhere throughout the board.
We hope to continue developing our Arcade-Simulator in the future. 

##Use of Pygame
Our pygame development is extensive in the sense that we did not just build one game in one file. We specifically developed this project to provide
easy addition of games in the future. This added to the complexity of our class hierarchy, but ultimately produced better coding style. The main 
configuration of pygame is housed in gamespace.py. The gameobj.py file acts as a wrapper for the sprite class. In this way the various sprites throughout
the arcade games can utilize the same pre-built functionality. The config.yaml and loader.py file act in tandem to initialize the pygame with the default
user setting specified in config.yaml. These can be investigated withing the game be pressing h in order to navigate to the help menu. main.py handles rendering 
the screen and housing the most basic high level gameplay calls.

In order to add new games, they should be developed under the modules folder. This is where snake.py resides as well as the initial development of pacman. This is
where unique images and items specific to the game are created. In the snake.py file we define the game loops for snake (with a multi player feature to add the other
players key strokes to the event loop using a network_data queue filled with data from dataReceived function of current player. This file also produces random food,
snake color, and movement of the snake depending on keystrokes. Similarly, the pacman.py file handles the sprite sheet in order to create pacman's movement and the
classic arcade background. 

##Use of Twisted
The majority of the Twisted protocol can be found in players.py. We build a peer to peer connection by having player one open up a listening port on localhost. Similarly
when player two boots up it will try to connect to this same port on localhost and begin passing data. The instantiation of these factories, as well as logic for 
single vs. multi-player can be found in gamespace.py. 
