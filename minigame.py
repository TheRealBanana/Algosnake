#############################
##       minigame.py       ##
## Simple snake mini-game  ##
#############################

from minigame_grids import countdown_3_grid, countdown_2_grid, countdown_1_grid, init_grid
from time import sleep

from PyQt4.QtCore import SIGNAL, QObject, QTimer

#Starting snake size, default 4
INIT_SNAKE_SIZE = 25

#Default starting grid
DEFAULT_START_GRID=(20,2)

#Thought about reusing the snake class I already wrote but I 
#need to replace practically all of the functions anyway.
class PlayerSnake(object):
    def __init__(self, context, start_grid=DEFAULT_START_GRID):
        self.context = context
        self.start_grid = start_grid
        #self.length tracks the length the snake is supposed to be
        self.length = INIT_SNAKE_SIZE
        #self.current_length tracks the size of the snake currently is
        self.current_length = 1
        #directions are r, l, u, and d
        self.direction = "r"
        

class MiniGame(object):
    def __init__(self, context):
        self.context = context
        self.MW = context.MainWindow
        self.uif = context.ui_functions
        self.snake = PlayerSnake(context)
        #Other crap
        self.number = 3
        self.countdown_timer = None
    
    def countdown(self):
        self.uif.resetGrid(minigame_override=True)
        if self.number > 0:
            countdown_grids = [countdown_1_grid, countdown_2_grid, countdown_3_grid]
            for grid, mode in countdown_grids[self.number-1][0].iteritems():
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
            print "And now we would let you play and sech, you know all that good stuff."
    
    def startButtonPressed(self):
        self.context.start_button.setEnabled(False)
        self.context.stop_button.setEnabled(True)
        self.countdown_timer = QTimer()
        QObject.connect(self.countdown_timer, SIGNAL("timeout()"), self.context.minigame.countdown)
        self.countdown_timer.start(1000)
        
    def stopButtonPressed(self):
        print "I would kill the game, but I'm too lazy. Just restart the damn thing."
        #Ideally we would now kill the game and reset back to algosnake mode.
    
    def initState(self):
        #Set up our initial grid and wait for the player to press the start button
        self.uif.resetGrid(minigame_override=True)
        for grid, mode in init_grid[0].iteritems():
            self.uif.setGridItem(grid, mode)
        self.MW.setWindowTitle("Algosnake :: Snake mini-game :: New Game :: Press Start")
        
        self.context.start_button.setEnabled(True)
        self.context.stop_button.setEnabled(False)
        self.context.clear_button.setEnabled(False)
        self.context.reset_button.setEnabled(False)
        
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
        
        
    def mainGameLoop(self):
        #Main loop here
        pass