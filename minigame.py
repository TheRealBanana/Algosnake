#############################
##       minigame.py       ##
## Simple snake mini-game  ##
#############################

from minigame_grids import countdown_3_grid, countdown_2_grid, countdown_1_grid, init_grid
from PyQt4.QtCore import SIGNAL, QObject, QTimer
from random import randint
from time import time

#Starting snake size, default 4
INIT_SNAKE_SIZE = 6

#starting snake update speed, in milliseconds. 
INIT_SNAKE_SPEED = 400

#How much the speed will be decreased every SPEED_INCREASE_BLOCKS objectives found
SPEED_MULTI = 0.90

#After how many blocks do we increase the speed of the snake?
SPEED_INCREASE_BLOCKS = 4

#Default starting grid
DEFAULT_START_GRID=(20, 2)

#Maximum number of objectives on the grid at once
MAX_OBJS = 10

#Number of objectives to add to the grid at start. This number has to be less than MAX_OBJS
NUM_START_OBJS = 3

#Number of seconds between adding/removing objectives from the grid
NEW_OBJ_INTERVAL = 4

COUNTDOWN_GRIDS = [countdown_1_grid, countdown_2_grid, countdown_3_grid]

#NEED TO ADD CONNECTIONS FOR ARROW KEYS
#CONNECT KEYS TO FUNCTION IN PlayerSnake OBJ, ChangeDirection().



#At the moment our snake grid is a fixed size and is very difficult to change
#I always wanted this to be resizable by the end user but I never implemented it.
#For now this has to correspond to the playable area, which right now is (25, 36).
GRID_BOUNDS = (25, 36)


#Just cause I know im dumb enough to mess this up and wonder why things suddenly dont work
if NUM_START_OBJS > MAX_OBJS: NUM_START_OBJS = MAX_OBJS

#Thought about reusing the snake class I already wrote but I 
#need to replace practically all of the functions anyway.
class PlayerSnake(object):
    def __init__(self, context, start_grid=DEFAULT_START_GRID):
        self.uif = context.ui_functions
        self.uif.invertGridColors()
        self.current_grid = start_grid
        #self.length tracks the length the snake is supposed to be
        self.length = INIT_SNAKE_SIZE
        
        #Actual grids the snake occupies currently
        #snake_grids[-1] is the snake head
        #snake_grids[0] is the snake tail
        self.snake_grids = [start_grid]
        
        #Objectives placed on the grid. Only MAX_OBJS will be shown at a time
        #New objectives are placed on the grid every NEW_OBJ_INTERVAL seconds
        #Each item is a simple tuple containing the grid coordinates.
        self.objective_list = []
        
        #directions are right, left, up, and down
        self.direction = "right"
        
        #Speed in milliseconds between updates
        self.speed = INIT_SNAKE_SPEED
        
        #If we hit a wall or ourselves, this changes to False.
        self.alive = False
        
    
    def getMove(self, direction=None):
        if direction is None: direction = self.direction
        
        if direction == "right":
            next_grid = (self.current_grid[0], self.current_grid[1]+1)
            
        elif direction == "left":
            next_grid = (self.current_grid[0], self.current_grid[1]-1)
            
        elif direction == "down":
            next_grid = (self.current_grid[0]+1, self.current_grid[1])
        
        elif direction == "up":
            next_grid = (self.current_grid[0]-1, self.current_grid[1])
        
        return next_grid
        
    
    def changeDirection(self, newdir):
        if self.alive == True:
            #Dont allow direction change in the direct opposite (run backwards)
            if self.getMove(newdir) != self.snake_grids[-2]:
                self.direction = newdir

    def collectedObj(self, grid):
        self.length += 1
        if (self.length - INIT_SNAKE_SIZE) % SPEED_INCREASE_BLOCKS == 0:
            self.speed = self.speed * SPEED_MULTI
            self.uif.MW.MainWindow.emit(SIGNAL("speedUpdated"))
        self.objective_list.remove(grid)
    
    def moveSnake(self):
        #Figure out the next grid from our current grid and our direction
        next_move = self.getMove()
        
        #Hit a wall, game over man. Game over!
        if ((0 <= next_move[0] <= GRID_BOUNDS[0]) and (0 <= next_move[1] <= GRID_BOUNDS[1])) is False:
            self.alive = False
        
        #Hit ourself! X(
        elif next_move in self.snake_grids:
            #Color the block we ran into red
            self.uif.setGridItem(next_move, 2)
            self.alive = False
        
        #good move
        else:
            #Move snake head, change old square color to snake body (state 7), cut off snake tail by changing to white if current snake size == max snake size
            self.uif.setGridItem(next_move, 3) #Snake head is state 3
            self.uif.setGridItem(self.current_grid, 7)
            
            self.snake_grids.append(next_move)
            
            #Check our length before we see if we collected an objective
            #Truncate our tail if we are too long
            if len(self.snake_grids) >= self.length:
                self.uif.setGridItem(self.snake_grids.pop(0), 0) #State 0 is white
            
            #see if we collected an objective (state 1)
            if next_move in self.objective_list:
                self.collectedObj(next_move)
            
            self.current_grid = next_move
        

class MiniGame(object):
    def __init__(self, context):
        self.context = context
        self.MW = context.MainWindow
        self.uif = context.ui_functions
        self.snake = PlayerSnake(context)
        #Other crap
        self.number = 3
        self.countdown_timer = None
        self.game_timer = None
        self.last_update_epoc = 0
    
    def countdown(self):
        self.uif.resetGrid(minigame_override=True)
        if self.number > 0:
            for grid, mode in COUNTDOWN_GRIDS[self.number-1][0].iteritems():
                self.uif.setGridItem(grid, mode)
            self.MW.setWindowTitle("Algosnake :: Snake mini-game :: Starting Game In %s" % self.number)
            self.number -= 1
        else:
            #Countdown finished, lets kill the timer
            self.countdown_timer.stop()
            self.countdown_timer = None
            
            self.MW.setWindowTitle("Algosnake :: Snake mini-game :: Playing")
            #Clear the grid and set our starting position to green
            self.uif.resetGrid(minigame_override=True)
            self.uif.setGridItem(DEFAULT_START_GRID, 3) #mode 3 is start position (green box)
            #Begin game
            self.game_timer.start()
    
    def startButtonPressed(self):
        #I tried using a simple loop with a sleep but it prevented the UI from updating. QTimer uses the signal/slot
        #system to launch its callable which doesn't block the main thread so it updates fine.
        self.countdown_timer = QTimer()
        QObject.connect(self.countdown_timer, SIGNAL("timeout()"), self.context.minigame.countdown)
        self.countdown_timer.start(1000)
        self.context.start_button.setEnabled(False)
        self.context.stop_button.setEnabled(True)
        self.context.game_grid.setFocus()
        
    def stopButtonPressed(self):
        print "I would kill the game, but I'm too lazy. Just restart the damn thing."
        #Ideally we would now kill the game and reset back to algosnake mode.
    
    def initState(self):
        #Lock the grid before anything
        self.uif.grid_locked = True
        self.context.game_grid.snakeGame = True
        
        #Set up our initial grid and wait for the player to press the start button
        self.uif.resetGrid(minigame_override=True)
        for grid, mode in init_grid[0].iteritems():
            self.uif.setGridItem(grid, mode)
        self.MW.setWindowTitle("Algosnake :: Snake mini-game :: New Game :: Press Start")
        
        self.context.start_button.setEnabled(True)
        self.context.stop_button.setEnabled(False)
        self.context.clear_button.setEnabled(False)
        self.context.reset_button.setEnabled(False)
        
        #Change the moves label to say "Score"
        
        
        #Disconnect the old start button connection and create a new one for our game
        QObject.disconnect(self.context.start_button, SIGNAL("clicked()"), self.context.ui_functions.startButtonPressed)
        QObject.disconnect(self.context.stop_button, SIGNAL("clicked()"), self.context.ui_functions.stopButtonPressed)
        #An important thing to note here for future reference.
        #When we tried to use self.startButtonPressed for the callable function below the connection failed.
        #However when we connected to the startButtonPressed function inside the instantiated version of the minigame it worked.
        #So in the future, when dealing with using class methods as callables in Qt connections, make sure you link to the
        #function using the instantiated object (don't use self.function, use self.context.object.function)
        #We'll have to do some testing to see if this is a hard and fast rule or if we can sometimes get around this.
        QObject.connect(self.context.start_button, SIGNAL("clicked()"), self.context.minigame.startButtonPressed)
        QObject.connect(self.context.stop_button, SIGNAL("clicked()"), self.context.minigame.stopButtonPressed)
        
        
        #Custom signals to manage gamestate changes
        self.game_timer = QTimer()
        self.updateGameTimerInterval()
        QObject.connect(self.game_timer, SIGNAL("timeout()"), self.context.minigame.mainGameLoop)
        QObject.connect(self.MW, SIGNAL("speedUpdated"), self.context.minigame.updateGameTimerInterval)
        QObject.connect(self.MW, SIGNAL("changeSnakeDirection"), self.context.minigame.snake.changeDirection)
        
    
    def updateGameTimerInterval(self):
        self.game_timer.setInterval(self.snake.speed)
    
    def mainGameLoop(self):
        #Main loop here
        #Before anything else lets populate the grid with a few objectives
        while len(self.snake.objective_list) < NUM_START_OBJS - 1:  #-1 because we add an objective at start by default, so dont count that one.
            self.addObjective()
        
        #First move
        if self.snake.alive == False and len(self.snake.snake_grids) == 1:
            self.snake.alive = True
        
        self.snake.moveSnake()
        
        #Check if our snake is alive or dead
        if self.snake.alive is False:
            self.gameOver()
        
        #Finally, add a new objective to the grid if enough time has past
        if time() - self.last_update_epoc > NEW_OBJ_INTERVAL:
            self.addObjective()
            self.last_update_epoc = time()
    
    def addObjective(self):
        #pick a random grid in the range of our current grid
        new_obj_grid = (randint(0, GRID_BOUNDS[0]), randint(0, GRID_BOUNDS[1]))
        #make sure its not a grid our snake occupies too.
        while new_obj_grid in self.snake.snake_grids:
            new_obj_grid = (randint(0, GRID_BOUNDS[0]), randint(0, GRID_BOUNDS[1]))
        #Ok found a good grid, make it an obj
        #First check if we need to remove an obj from the grid
        if len(self.snake.objective_list) == MAX_OBJS:
            #Remove the oldest objective from the grid
            self.uif.setGridItem(self.snake.objective_list.pop(0), 0) #State 0 is white
            
        self.uif.setGridItem(new_obj_grid, 1)
        self.snake.objective_list.append(new_obj_grid)
        
    
    def gameOver(self):
        self.game_timer.stop()
        print "GAME OVER MAN!"
        print "Final Score: %s" % len(self.snake.snake_grids)
        print "Better luck next time!"
        #self.resetMode()
        