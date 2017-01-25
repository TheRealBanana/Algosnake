##############################
##  Algosnake UI Functions  ##
##############################
from PyQt4 import QtGui, QtCore
from time import time, sleep
from random import randint
from PyQt4.QtCore import SIGNAL
import threading
import cPickle
import os

#Default tick rate of once per second
TICKRATE_MS = 1000

class RunInstance(threading.Thread):
    def __init__(self, snake, context):
        self.quitting = False
        self.context = context
        self.snake = snake
        self.last_tick = time()
        self.last_clock_update = time()
        self.clock_timer = 0
        # Memory algo vars
        self.past_moves = None
        self.backtracking = False
        
        
        super(RunInstance, self).__init__()


    def run(self):
        while self.quitting is False:
            if self.context.start_grid == None:
                print "NO START POINT SET!"
                #unlock grid to allow setting of start
                self.context.grid_locked = False
                self.context.MW.start_button.setEnabled(True)
                self.context.MW.stop_button.setEnabled(False)
                self.quitting = True
                continue
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
            elif current_algo == "Backtrack with memory - straight until obstructed":
                self.backtrack_with_memory()
            else:
                self.random_move_nometric()
            
            if self.snake.found_all == True:
                print "FOUND THEM ALL, WE'RE DONE!"
                self.context.MW.stop_button.setEnabled(False)
                self.quitting = True
        
        
    def random_move_nometric(self):
        #Get our list of moves
        possible_moves = self.snake.getMoves()
        move_selection = []
        for direction, move_infos in possible_moves.iteritems():
            if move_infos[0] is not None:
                move_selection.append(move_infos[0])
        #Choose a random move
        our_move = move_selection[randint(0, len(move_selection)-1)]
        self.snake.moveSnake(our_move)
        
        
    def random_move_nometric_prefernew(self):
        #Get our list of moves
        possible_moves = self.snake.getMoves()
        move_selection = []
        preferred_moves = []
        for direction, move_infos in possible_moves.iteritems():
            if move_infos[0] is not None:
                #Prefer objective, then fresh grid, then old grid
                if move_infos[1] == 1:
                    #If we find an objective, break out of the move seek and set the preferred moves to just the objective's grid
                    preferred_moves = [move_infos[0]]
                    break
                elif move_infos[1] == 0:
                    preferred_moves.append(move_infos[0])
                else:
                    move_selection.append(move_infos[0])
        #Choose a random move, prefer new boxes
        if len(preferred_moves) > 0:
            our_move = preferred_moves[randint(0, len(preferred_moves)-1)]
        else:
            our_move = move_selection[randint(0, len(move_selection)-1)]
        self.snake.moveSnake(our_move)
        
    def backtrack_with_memory(self):
        #First move?
        if self.past_moves is None:
            self.past_moves = []
            self.backtracking = False
            self.snake.direction = "START"
        
        possible_moves = self.snake.getMoves()
        #For this one we want to concentrate on only the blue and white blocks, avoiding any block we've visited previously unless absolutely necessary (backtracking)
        white_blocks = {}
        blue_blocks = []
        for direction, move in possible_moves.iteritems():
            if move[0] is not None:
                if move[1] == 0:
                    white_blocks[direction] = move
                if move[1] == 1:
                    blue_blocks.append([move, direction])
        #No more good moves, backtrack one move
        if len(white_blocks) == 0 and len(blue_blocks) == 0:
            self.backtracking = True
            move_direction = "BT"
            our_move = self.past_moves.pop(-1)
            print "BACKTRACKING..."
            
        #Blue moves first, then white.
        elif len(blue_blocks) > 0:
            self.backtracking = False
            our_move = blue_blocks.pop(0) #Take the first one
            move_direction = our_move[1]
            our_move = our_move[0][0]
        elif len(white_blocks) > 0:
            self.backtracking = False
            #Pick first choice given to us if its the start or we can't continue on in the same direction as before
            if self.snake.direction == "START" or white_blocks.has_key(self.snake.direction) is False:
                move_direction = white_blocks.keys()[0]
                our_move = white_blocks[move_direction][0]
            else:
                our_move = white_blocks[self.snake.direction][0]
                move_direction = self.snake.direction
            del(white_blocks[move_direction])
        
        #Make our move and update our direction of travel
        if self.backtracking == False:
            self.past_moves.append(self.snake.current_grid)
        
        self.snake.direction = move_direction
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
        self.direction = "NOTUSED"
    
    def getMoves(self):
        #this function returns all available moves
        #Only support up down left and right for now, no diagonal.
        moves = {}
        
        try:
            moves["up"] = [(self.current_grid[0]-1, self.current_grid[1]), self.grid_item_tracker[(self.current_grid[0]-1, self.current_grid[1])]]
            if moves["up"][1] == 2: #Roadblock
                moves["up"] = [None, None]
        except:
            moves["up"] = [None, None]
        try:
            moves["down"] = [(self.current_grid[0]+1, self.current_grid[1]), self.grid_item_tracker[(self.current_grid[0]+1, self.current_grid[1])]]
            if moves["down"][1] == 2: #Roadblock
                moves["down"] = [None, None]
        except:
            moves["down"] = [None, None]
        try:
            moves["left"] = [(self.current_grid[0], self.current_grid[1]-1), self.grid_item_tracker[(self.current_grid[0], self.current_grid[1]-1)]]
            if moves["left"][1] == 2: #Roadblock
                moves["left"] = [None, None]
        except:
            moves["left"] = [None, None]
        try:
            moves["right"] = [(self.current_grid[0], self.current_grid[1]+1), self.grid_item_tracker[(self.current_grid[0], self.current_grid[1]+1)]]
            if moves["right"][1] == 2: #Roadblock
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
        
        #Emit signal to update number of moves
        self.context.MW.MainWindow.emit(SIGNAL("snakeMoved"))
        
        
        
    
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
        self.start_grid = None
        self.clock_timer = 0
        self.total_objectives = 0
        self.total_moves = 0
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
    
    
    def incrementMoveCount(self):
        #Increment move count
        self.total_moves += 1
        self.MW.moves_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">%s</span></p></body></html>" % self.total_moves)
    
    def resetGrid(self):
        #Stop any current run
        try:
            self.stopButtonPressed()
        except:
            pass
        #Loop through each grid item and set it to default
        for row in range(0, self.grid_size[0] + 1):
            for column in range(0, self.grid_size[1] + 1):
                default_grid_item = QtGui.QTableWidgetItem()
                default_grid_item.setBackground(self.grid_item_states[0])
                self.MW.game_grid.setItem(row, column, default_grid_item)
                self.grid_item_tracker[(row,column)] = 0
        self.start_grid = None
        #Reset time, found, and moves count to zero
        self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0</span></p></body></html>")
        self.MW.time_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">00:00</span></p></body></html>")
        self.MW.moves_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">0</span></p></body></html>")
        self.clock_timer = 0
        self.total_objectives = 0
        self.total_moves = 0
        #Finally unlock the grid
        self.grid_locked = False
        
    
    
    def setGridItem(self, grid, new_mode):
        new_start_grid_item = self.MW.game_grid.item(*grid)
        old_grid_mode = self.grid_item_tracker[grid]
        #Decrement objective if it was set
        if old_grid_mode == 1:
            self.total_objectives -= 1
            self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/%s</span></p></body></html>" % self.total_objectives)
        
        #Reset start position
        elif old_grid_mode == 3:
            self.start_grid = None

        #increment new objective
        if new_mode == 1:
            self.total_objectives += 1
            self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/%s</span></p></body></html>" % self.total_objectives)
        
        #Setting new start position
        elif new_mode == 3:
            #reset old start grid if necessary
            if self.start_grid is not None:
                old_start_grid_item = self.MW.game_grid.item(self.start_grid[0], self.start_grid[1])
                old_start_grid_item.setBackground(self.grid_item_states[0])
                self.grid_item_tracker[(self.start_grid[0], self.start_grid[1])] = 0
            #set new start grid
            self.start_grid = (grid[0], grid[1])
        
        #Finally update tracker and update new item background
        self.grid_item_tracker[(grid[0], grid[1])] = new_mode
        new_start_grid_item.setBackground(self.grid_item_states[new_mode])
    
    
    def itemClicked(self, row, column):
        if self.grid_locked == True:
            return
        
        qapp = QtGui.QApplication.instance()
        keyboard_mods = qapp.queryKeyboardModifiers()
        #holding control key to set start grid
        if keyboard_mods == QtCore.Qt.ControlModifier:
            self.setGridItem((row, column), 3)
        #Holding shift sets a roadblock
        elif keyboard_mods == QtCore.Qt.ShiftModifier:
            self.setGridItem((row, column), 2)
        #Normal click
        else:   
            #Toggle straight to off from all blocks
            if self.grid_item_tracker[(row,column)] >= 1:
                self.setGridItem((row, column), 0)
            else:
                self.setGridItem((row, column), 1)
    
    def startButtonPressed(self):
        self.updateSpeed()
        
        snake_instance = Snake(self.start_grid, self.grid_item_states, self.MW.game_grid, self.grid_item_tracker, self)
        self.game_instance_thread = RunInstance(snake_instance, self)
        self.game_instance_thread.start()
        self.grid_locked = True
        self.MW.start_button.setEnabled(False)
        self.MW.stop_button.setEnabled(True)
    
    def stopButtonPressed(self):
        self.game_instance_thread.quitting = True
        self.game_instance_thread.join()
        self.start_grid = self.game_instance_thread.snake.current_grid
        self.grid_item_tracker[self.game_instance_thread.snake.current_grid] = 3
        self.MW.start_button.setEnabled(True)
        self.MW.stop_button.setEnabled(False)
        self.grid_locked = False
        print "ROUND STOPPED"
    
    
    def stopAndQuit(self):
        try:
            self.stopButtonPressed()
        except:
            pass
        self.MW.MainWindow.close()
    
    def updateSpeed(self):
        global TICKRATE_MS
        #Figure out speed
        #                High speeds 11-20             Low speeds 1-10
        speeds = [x for x in range(10, 110, 10)] + [x for x in range(100, 1100, 100)]
        speeds.reverse()
        TICKRATE_MS = speeds[self.MW.speed_selector.value()-1]
        
    
    def fileDialogMaster(self, main_mode, file_mode, dialog_caption, filters="Algosnake Grid (*.gridstate)"):
        start_dir = os.getcwd()
        print start_dir
        fileDialog = QtGui.QFileDialog()
        fileDialog.AcceptMode = main_mode
        fileDialog.setDirectory(start_dir)
        fileDialog.setFileMode(file_mode)
        if main_mode == QtGui.QFileDialog.AcceptOpen:
            chosenFile = fileDialog.getOpenFileName(caption=dialog_caption, filter=filters)
        else:
            chosenFile = fileDialog.getSaveFileName(caption=dialog_caption, filter=filters)
        
        return chosenFile
    
    
    #We're not doing any checking, just save and load. We pickle the data just to add some basic level of data integrity checking.
    def saveGrid(self):
        savefilepath = self.fileDialogMaster(QtGui.QFileDialog.AcceptSave, QtGui.QFileDialog.AnyFile, "Save Current Grid...")
        
        if len(savefilepath) > 0:
            savedata = [self.grid_item_tracker, self.start_grid]
            savedata = cPickle.dumps(savedata)
            
            with open(savefilepath, "w") as savefile:
                savefile.write(savedata)
        
    
    def loadGrid(self):
        #Stop if currently running
        try:
            self.stopButtonPressed()
        except:
            pass
        
        loadfilepath = self.fileDialogMaster(QtGui.QFileDialog.AcceptOpen, QtGui.QFileDialog.ExistingFile, "Load Saved Grid...")
        
        if len(loadfilepath) > 0:
            with open(loadfilepath, "r") as loadedfile:
                loadeddata = loadedfile.read()
            try:
                griddata = cPickle.loads(loadeddata)
            except:
                print "Invalid grid file!"
                return
        else:
            return
        #reset current grid before loading new one
        self.resetGrid()
        
        
        self.start_grid = griddata[1]
        self.grid_item_tracker = griddata[0]
        
        #Set up the grid and count objectives
        for grid, mode in self.grid_item_tracker.iteritems():
            if mode == 1:
                self.total_objectives += 1
            self.setGridItem(grid, mode)
