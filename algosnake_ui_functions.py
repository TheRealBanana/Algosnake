##############################
##  Algosnake UI Functions  ##
##############################
from PyQt4 import QtGui, QtCore
from time import time, sleep
from random import randint
import threading

TICKRATE_MS = 100

class RunInstance(threading.Thread):
    def __init__(self, snake, context):
        self.quitting = False
        self.context = context
        self.snake = snake
        self.last_tick = time()
        self.last_clock_update = time()
        super(RunInstance, self).__init__()


    def run(self):
        print "THREAD START!"
        while self.quitting is False:
            sleep(float(TICKRATE_MS/float(1000)))
            print "TICK"
            #Update clock if necessary
            if time() - self.last_clock_update >= 1:
                print "UPDATE_CLOCK_PLACEHOLDER"
                self.last_clock_update = time()
            
            
            #Choose your algo here:
            self.random_move_nometric()
        
        print "QUITTING...."
        
        
    def random_move_nometric(self):
        #Get our list of moves
        possible_moves = self.snake.getMoves()
        move_selection = []
        for direction, move_infos in possible_moves.iteritems():
            print "%s:%s:%s" % (direction, move_infos[0], move_infos[1])
            if move_infos[0] is not None:
                print "APPENDING MOVE...."
                move_selection.append(move_infos[0])
        #Choose a random move
        our_move = move_selection[randint(0, len(move_selection)-1)]
        self.snake.moveSnake(our_move)
        

class Snake(object):
    def __init__(self, start_grid, grid_item_states, game_grid, grid_item_tracker):
        self.start_grid = start_grid
        self.current_grid = start_grid
        self.game_grid = game_grid
        self.grid_item_tracker = grid_item_tracker
        self.grid_item_states = grid_item_states
        self.collected_objectives = 0
    
    def getMoves(self):
        #this function returns all available moves
        #Only support up down left and right for now, no diagonal.
        moves = {}
        
        try:
            moves["up"] = [(self.current_grid[0]-1, self.current_grid[1]), self.grid_item_tracker[(self.current_grid[0]-1, self.current_grid[1])]]
            if moves["up"][1] == 2:
                print "ROADBLOCK ABOVE"
                moves["up"] = [None, None]
        except Exception as e:
            print "EXCEPTED:\n%s" % e
            moves["up"] = [None, None]
        try:
            moves["down"] = [(self.current_grid[0]+1, self.current_grid[1]), self.grid_item_tracker[(self.current_grid[0]+1, self.current_grid[1])]]
            if moves["down"][1] == 2:
                print "ROADBLOCK BELOW"
                moves["down"] = [None, None]
        except:
            moves["down"] = [None, None]
        try:
            moves["left"] = [(self.current_grid[0], self.current_grid[1]-1), self.grid_item_tracker[(self.current_grid[0], self.current_grid[1]-1)]]
            if moves["left"][1] == 2:
                print "ROADBLOCK LEFT"
                moves["left"] = [None, None]
        except:
            moves["left"] = [None, None]
        try:
            moves["right"] = [(self.current_grid[0], self.current_grid[1]+1), self.grid_item_tracker[(self.current_grid[0], self.current_grid[1]+1)]]
            if moves["right"][1] == 2:
                print "ROADBLOCK RIGHT"
                moves["right"] = [None, None]
        except:
            moves["right"] = [None, None]
            
        return moves
        
    
    def moveSnake(self, new_grid):
        #color our old grid dark grey and set its state to number 5 (past position)
        current_grid_item = self.game_grid.item(*self.current_grid)
        current_grid_item.current_mode = 5
        current_grid_item.setBackground(self.grid_item_states[5])
        #Update new grid with our position color
        new_grid_item = self.game_grid.item(*new_grid)
        #Check if we found an objective
        if new_grid_item.current_mode == 1:
            self.foundObjective()
        new_grid_item.current_mode = 4
        new_grid_item.setBackground(self.grid_item_states[4])
        self.current_grid = new_grid
        
    
    def foundObjective(self):
        self.collected_objectives += 1
        print "UPDATE_COUNT_PLACEHOLDER"
        
    
class uiFunctions(object):
    def __init__(self, MW_ref):
        self.MW = MW_ref
        self.game_instance_thread = None
        self.grid_item_tracker = {}
        self.grid_item_states = {}
        self.grid_locked = False
        self.grid_size = (25, 36)
        self.start_grid = (0,0)
        self.current_grid = None
        #default
        self.grid_item_states[0] = QtGui.QBrush(QtGui.QColor(255, 255, 255, 255))
        #objective
        self.grid_item_states[1] = QtGui.QBrush(QtGui.QColor(0, 84, 166, 255))
        #roadblock
        self.grid_item_states[2] = QtGui.QBrush(QtGui.QColor(255, 0, 0, 255))
        #start
        self.grid_item_states[3] = QtGui.QBrush(QtGui.QColor(66, 255, 0, 255))
        #current position
        self.grid_item_states[4] = QtGui.QBrush(QtGui.QColor(66, 255, 0, 255)) #Keeping to allow changing current position color more easily in the future
        #past position
        self.grid_item_states[5] = QtGui.QBrush(QtGui.QColor(85, 85, 85, 255))
    
    
    def resetGrid(self):
        #Loop through each grid item and set it to default
        for row in range(0, self.grid_size[0] + 1):
            for column in range(0, self.grid_size[1] + 1):
                default_grid_item = QtGui.QTableWidgetItem()
                default_grid_item.setBackground(self.grid_item_states[0])
                self.MW.game_grid.setItem(row, column, default_grid_item)
                default_grid_item.current_mode = 0
                self.grid_item_tracker[(row,column)] = 0
        self.start_grid = None
        #Reset time and found count to zero
        self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0</span></p></body></html>")
        self.MW.time_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">00:00</span></p></body></html>")
        #Finally unlock the grid
        self.grid_locked = False
    
    def itemClicked(self, row, column):
        print "(%s,%s)" % (row, column)
        qapp = QtGui.QApplication.instance()
        keyboard_mods = qapp.queryKeyboardModifiers()
        #holding control key to set start grid
        if keyboard_mods == QtCore.Qt.ControlModifier:
            #reset old start grid
            if self.start_grid is not None:
                default_grid_item = QtGui.QTableWidgetItem()
                default_grid_item.setBackground(self.grid_item_states[0])
                self.MW.game_grid.setItem(self.start_grid[0], self.start_grid[1], default_grid_item)
            #Set new start point
            start_grid_item = QtGui.QTableWidgetItem()
            start_grid_item.setBackground(self.grid_item_states[3])
            self.MW.game_grid.setItem(row, column, start_grid_item)
            self.grid_item_tracker[self.start_grid] = 0
            self.start_grid = (row, column)
            self.grid_item_tracker[self.start_grid] = 3
            start_grid_item.current_mode = 3
        else:
            if self.grid_locked == False:
                #Get QTableWidgetItem
                selected_grid_item = self.MW.game_grid.item(row, column)
                #Set default mode if it doesn't already exist
                if hasattr(selected_grid_item, "current_mode") is False:
                    selected_grid_item.current_mode = 0
                    self.grid_item_tracker[(row,column)] = 0
                if selected_grid_item.current_mode == 3:
                    self.start_grid = None
                    
                #wrap
                if selected_grid_item.current_mode > 1:
                    selected_grid_item.current_mode = 0
                    self.grid_item_tracker[(row,column)] = 0
                else:
                    selected_grid_item.current_mode += 1
                    self.grid_item_tracker[(row,column)] += 1
                #set mode
                selected_grid_item.setBackground(self.grid_item_states[self.grid_item_tracker[(row,column)]])
                
    
    def startButtonPressed(self):
        print "HERE 3"
        snake_instance = Snake(self.start_grid, self.grid_item_states, self.MW.game_grid, self.grid_item_tracker)
        self.game_instance_thread = RunInstance(snake_instance, self)
        self.game_instance_thread.start()
        #Lets use a plain old threading.Thread object to handle the snake movement
    
    def stopbuttonPressed(self):
        print "HERE 4"
        self.game_instance_thread.quitting = True
        self.game_instance_thread.join()
        print "GAME JOINED"
    