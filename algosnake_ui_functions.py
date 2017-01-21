##############################
##  Algosnake UI Functions  ##
##############################
from PyQt4 import QtGui, QtCore
from time import time, sleep
from random import randint
import threading

TICKRATE_MS = 500

class RunInstance(threading.Thread):
    def __init__(self, snake, context):
        self.quitting = False
        self.context = context
        self.snake = snake
        self.last_tick = time()
        self.last_clock_update = time()
        self.clock_timer = 0
        super(RunInstance, self).__init__()


    def run(self):
        print "THREAD START!"
        while self.quitting is False:
            sleep(float(TICKRATE_MS/float(1000)))
            #Update clock if necessary
            if time() - self.last_clock_update >= 1:
                self.last_clock_update = time()
                self.context.updateClock()
            
            
            #Get current algo, default to random
            current_algo_item = self.context.MW.algoList.currentItem()
            try:
                current_algo = current_algo_item.text()
            except:
                current_algo = ""
            
            if current_algo == "Random - Prefer Unexplored":
                self.random_move_nometric_prefernew()
            else:
                self.random_move_nometric()
            
            if self.snake.found_all == True:
                print "FOUND THEM ALL, WE'RE DONE!"
                self.quitting = True
                
        
        print "QUITTING...."
        
        
    def random_move_nometric(self):
        #Get our list of moves
        possible_moves = self.snake.getMoves()
        move_selection = []
        for direction, move_infos in possible_moves.iteritems():
            if move_infos[0] is not None:
                move_selection.append(move_infos[0])
        #Choose a random move
        try:
            our_move = move_selection[randint(0, len(move_selection)-1)]
        except:
            print "NO START POINT SET!"
            self.quitting = True
            return
        self.snake.moveSnake(our_move)
        
        
    def random_move_nometric_prefernew(self):
        #Get our list of moves
        possible_moves = self.snake.getMoves()
        move_selection = []
        preferred_moves = []
        for direction, move_infos in possible_moves.iteritems():
            if move_infos[0] is not None:
                if move_infos[1] == 0:
                    print "FOUND PREFERRED MOVE"
                    preferred_moves.append(move_infos[0])
                else:
                    move_selection.append(move_infos[0])
        #Choose a random move, prefer new boxes
        if len(preferred_moves) > 0:
            print "PREFERRED MOVE EXEC"
            our_move = preferred_moves[randint(0, len(preferred_moves)-1)]
        else:
            print "CRAP MOVE EXEC"
            our_move = move_selection[randint(0, len(move_selection)-1)]
        self.snake.moveSnake(our_move)
        

class Snake(object):
    def __init__(self, start_grid, grid_item_states, game_grid, grid_item_tracker, context):
        self.start_grid = start_grid
        self.current_grid = start_grid
        self.game_grid = game_grid
        self.grid_item_tracker = grid_item_tracker
        self.grid_item_states = grid_item_states
        self.collected_objectives = 0
        self.found_all = False
        self.context = context
    
    def getMoves(self):
        #this function returns all available moves
        #Only support up down left and right for now, no diagonal.
        moves = {}
        
        try:
            moves["up"] = [(self.current_grid[0]-1, self.current_grid[1]), self.grid_item_tracker[(self.current_grid[0]-1, self.current_grid[1])]]
            if moves["up"][1] == 2:
                print "ROADBLOCK ABOVE"
                moves["up"] = [None, None]
        except:
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
        #Check if we found an objective
        if self.grid_item_tracker[new_grid] == 1:
            self.foundObjective()
        
        #color our old grid dark grey and set its state to number 5 (past position)
        current_grid_item = self.game_grid.item(*self.current_grid)
        self.grid_item_tracker[self.current_grid] = 5
        current_grid_item.setBackground(self.grid_item_states[5])
        
        #Update new grid with our position color
        new_grid_item = self.game_grid.item(*new_grid)
        self.grid_item_tracker[new_grid] = 4
        new_grid_item.setBackground(self.grid_item_states[4])
        self.current_grid = new_grid
        
        
    
    def foundObjective(self):
        print "FOUND OBJ!"
        self.collected_objectives += 1
        self.context.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">%s/%s</span></p></body></html>" % (self.collected_objectives, self.context.total_objectives))
        if self.collected_objectives == self.context.total_objectives:
            self.found_all = True
        
    
class uiFunctions(object):
    def __init__(self, MW_ref):
        self.MW = MW_ref
        self.game_instance_thread = None
        self.grid_item_tracker = {}
        self.grid_item_states = {}
        self.grid_locked = False
        self.grid_size = (25, 36)
        self.start_grid = (0,0)
        self.clock_timer = 0
        self.total_objectives = 0
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
    
    
    def updateClock(self):
        self.clock_timer += 1
        minutes = self.clock_timer/60
        seconds = self.clock_timer%60
        self.MW.time_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">%02d:%02d</span></p></body></html>" % (minutes, seconds))
    
    
    def resetGrid(self):
        #Loop through each grid item and set it to default
        for row in range(0, self.grid_size[0] + 1):
            for column in range(0, self.grid_size[1] + 1):
                default_grid_item = QtGui.QTableWidgetItem()
                default_grid_item.setBackground(self.grid_item_states[0])
                self.MW.game_grid.setItem(row, column, default_grid_item)
                self.grid_item_tracker[(row,column)] = 0
        self.start_grid = None
        #Reset time and found count to zero
        self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0</span></p></body></html>")
        self.MW.time_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">00:00</span></p></body></html>")
        #Finally unlock the grid
        self.grid_locked = False
        self.clock_timer = 0
        
    
    def itemClicked(self, row, column):
        print "(%s,%s)" % (row, column)
        if self.grid_locked == True:
            return
        qapp = QtGui.QApplication.instance()
        keyboard_mods = qapp.queryKeyboardModifiers()
        #holding control key to set start grid
        if keyboard_mods == QtCore.Qt.ControlModifier:
            if self.grid_item_tracker[(row,column)] == 1:
                self.total_objectives -= 1
                self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/%s</span></p></body></html>" % self.total_objectives)
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
        elif keyboard_mods == QtCore.Qt.ShiftModifier:
            if self.grid_item_tracker[(row,column)] == 1:
                self.total_objectives -= 1
                self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/%s</span></p></body></html>" % self.total_objectives)
            selected_grid_item = self.MW.game_grid.item(row, column)
            self.grid_item_tracker[(row,column)] = 2
            selected_grid_item.setBackground(self.grid_item_states[self.grid_item_tracker[(row,column)]])
        else:
            #Get QTableWidgetItem
            selected_grid_item = self.MW.game_grid.item(row, column)
            if self.grid_item_tracker[(row,column)] == 3:
                self.start_grid = None
                
            #wrap
            if self.grid_item_tracker[(row,column)] >= 1:
                if self.grid_item_tracker[(row,column)] == 1:
                    self.total_objectives -= 1
                self.grid_item_tracker[(row,column)] = 0
                
            else:
                self.grid_item_tracker[(row,column)] = 1
                self.total_objectives += 1
            #set mode
            selected_grid_item.setBackground(self.grid_item_states[self.grid_item_tracker[(row,column)]])
            #update obj count if changed
            self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/%s</span></p></body></html>" % self.total_objectives)
    
    def startButtonPressed(self):
        print "START_GRID: %s" % repr(self.start_grid)
        snake_instance = Snake(self.start_grid, self.grid_item_states, self.MW.game_grid, self.grid_item_tracker, self)
        self.game_instance_thread = RunInstance(snake_instance, self)
        self.game_instance_thread.start()
        self.grid_locked = True
        #Lets use a plain old threading.Thread object to handle the snake movement
    
    def stopbuttonPressed(self):
        self.game_instance_thread.quitting = True
        self.game_instance_thread.join()
        self.start_grid = self.game_instance_thread.snake.current_grid
        self.grid_item_tracker[self.game_instance_thread.snake.current_grid] = 3
        print "ROUND STOPPED"
    