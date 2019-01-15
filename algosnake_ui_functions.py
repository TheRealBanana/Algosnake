##############################
##  Algosnake UI Functions  ##
##############################
from PyQt4 import QtGui, QtCore, Qt
from time import time, sleep
from random import randint
from PyQt4.QtCore import SIGNAL
from copy import deepcopy as DC
from collections import OrderedDict as OD
from math import sqrt
from itertools import product as itertools_product
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
        self.decision_points = None
        self.backtracking = False
        self.last_hl_grid = None
        
        
        super(RunInstance, self).__init__()


    def run(self):
        #Get current algo, default to random
        current_algo_item = self.context.MW.algoList.currentItem()
        if current_algo_item.text() == "Pathfinder 1 (Depth-first)":
            self.pathfinder_1(metric=False)
        elif current_algo_item.text() == "Pathfinder 1 (Depth-first w/metric)":
            self.pathfinder_1(metric=True)
        elif current_algo_item.text() == "A*":
            self.a_star()

        else:
            while self.quitting is False:
                if self.context.start_grid == None:
                    print "NO START POINT SET!"
                    self.quitting = True
                    #unlock grid
                    self.context.MW.MainWindow.emit(SIGNAL("unlockGrid"))
                    self.context.MW.MainWindow.emit(SIGNAL("LockControls"), False)
                    continue
                elif self.context.finish_grid is None and self.context.total_objectives == 0:
                    print "NO FINISH GRID OR OBJECTIVES SET, YOU MUST SET SOMETHING!"
                    self.quitting = True
                    #unlock grid
                    self.context.MW.MainWindow.emit(SIGNAL("unlockGrid"))
                    self.context.MW.MainWindow.emit(SIGNAL("LockControls"), False)
                    continue
                sleep(float(TICKRATE_MS/float(1000)))
                #Update clock if necessary
                if time() - self.last_clock_update >= 1:
                    self.last_clock_update = time()
                    self.context.updateClock()



                try:
                    current_algo = current_algo_item.text()
                except:
                    current_algo = ""

                if current_algo == "Random - Prefer Unexplored":
                    self.random_move_nometric_prefernew()
                elif current_algo == "Backtrack with memory - straight until obstructed":
                    self.backtracker()
                elif current_algo == "Backtracker - Shortcutter":
                    self.backtracker_shortcuter()
                elif current_algo == "Backtracker - Shortcutter - Prefer largest cut":
                    self.backtracker_shortcuter(mode="distance")
                elif current_algo == "Backtracker - Shortcutter w/ Metric":
                    self.backtracker_shortcuter(mode="metric")
                else:
                    self.random_move_nometric()

                if self.snake.found_all == True:
                    print "FOUND THEM ALL, WE'RE DONE!"
                    self.context.MW.MainWindow.emit(QtCore.SIGNAL("LockControls"), False)
                    #self.context.MW.start_button.setEnabled(True)
                    self.quitting = True
                elif self.snake.found_finish == True:
                    print "TOTAL TIME TO FINISH: %s seconds" % self.context.clock_timer
                    self.context.MW.MainWindow.emit(QtCore.SIGNAL("LockControls"), False)
                    #self.context.MW.start_button.setEnabled(True)
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
                if move_infos[1] == 1 or move_infos[1] == 6:
                    #If we find an objective or finish, break out of the move seek and set the preferred moves to just the objective/finish grid
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
        
    def backtracker(self):
        #First move?
        if self.past_moves is None:
            self.past_moves = []
            self.backtracking = False
            self.snake.direction = "START"
            print "[0] SEEKING [0]..."
        
        possible_moves = self.snake.getMoves()
        #For this one we want to concentrate on only the blue and white blocks, avoiding any block we've visited previously unless absolutely necessary (backtracking)
        white_blocks = {}
        blue_blocks = []
        for direction, move in possible_moves.iteritems():
            if move[0] is not None:
                if move[1] == 0:
                    white_blocks[direction] = move
                #We treat the finish block like the blue blocks for all intents and purposes
                if move[1] == 1 or move[1] == 6:
                    blue_blocks.append([move, direction])
        #No more good moves, backtrack one move
        if len(white_blocks) == 0 and len(blue_blocks) == 0:
            if self.backtracking is False:
                print "[Move %s] BACKTRACKING [%s]..." % (self.context.total_moves, len(self.past_moves))
            self.backtracking = True
            move_direction = "BT"
            our_move = self.past_moves.pop(-1)
            
            
        #Blue moves first, then white.
        elif len(blue_blocks) > 0:
            if self.backtracking is True:
                print "[Move %s] SEEKING [%s]..." % (self.context.total_moves, len(self.past_moves))
            self.backtracking = False
            our_move = blue_blocks.pop(0) #Take the first one
            move_direction = our_move[1]
            our_move = our_move[0][0]
        elif len(white_blocks) > 0:
            if self.backtracking is True:
                print "[Move %s] SEEKING [%s]..." % (self.context.total_moves, len(self.past_moves))
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
        
    def backtracker_shortcuter(self, mode="first"):
        #Modes:
        #First - Takes first available shortcut (Default)
        #Distance - Chooses the largest shortcut
        #Metric - Checks whether the move is closer or farther from the previous decision point
        #First move?
        if self.past_moves is None:
            self.past_moves = []
            self.decision_points = OD()
            self.backtracking = False
            self.snake.direction = "START"
            print "[0] SEEKING [0]..."
        
        possible_moves = self.snake.getMoves()
        #For this one we want to concentrate on only the blue and white blocks
        #Unlike the backtracker we will accept a grey move that is is in our
        #past_moves and is between us and the last decision point.
        white_blocks = {}
        blue_blocks = []
        grey_blocks = []
        move_direction = None
        our_move = None
        
        #Prune up our decision points
        for decision_point, grid_list in self.decision_points.iteritems():
            if self.snake.current_grid in grid_list:
                self.decision_points[decision_point].pop(grid_list.index(self.snake.current_grid))
                #If that was the last move for this decision point, remove it from the dict
                if len(self.decision_points[decision_point]) == 0:
                    del(self.decision_points[decision_point])
        
        for direction, move in possible_moves.iteritems():
            if move[0] is not None:
                if move[1] == 0:
                    white_blocks[direction] = move
                if move[1] == 1 or move[1] == 6:
                    blue_blocks.append([move, direction])
                if move[1] == 5:
                    grey_blocks.append(move)
        
        
        #No more good moves, check if we got a good grey move or not, backtrack if not
        if len(white_blocks) == 0 and len(blue_blocks) == 0:
            #Check for shortcuts
            if len(grey_blocks) > 0:
                #Figure out how far to slice back in our past_moves
                try:
                    last_decision_point = self.decision_points.keys()[-1]
                except:
                    pass
                else:
                    last_decision_point_index = self.past_moves.index(last_decision_point)
                    shortcut_slice = self.past_moves[last_decision_point_index:-1] #Ignore our last move, otherwise we are just backtracking
                    
                    possible_shortcuts = []
                    for grid in grey_blocks:
                        if grid[0] in shortcut_slice:
                            possible_shortcuts.append(grid[0])
                    
                    if len(possible_shortcuts) > 0:
                        #Take the first shortcut we find, no preference
                        if mode.lower() == "first":
                            our_move = possible_shortcuts[0]
                        
                        #Choose the largest shortcut
                        #Not sure this works the way we intended.....
                        elif mode.lower() == "distance":
                            sorted_index_list = [self.past_moves.index(i) for i in possible_shortcuts]
                            sorted_index_list.sort()
                            #largest shortcut is the farthest back in our past_moves
                            our_move = self.past_moves[sorted_index_list[0]]
                        
                        elif mode.lower() == "metric":
                            #Check distance between the last decision point and each possible move
                            #and chose the move that gets us closest.
                            distances = {}
                            #Now I wish I paid more attention in math class... :(
                            for grid in possible_shortcuts:
                                #Shouldnt these be swapped? Shouldn't t1 use index 0 of grid and last_decision_point since its the x val?
                                #first term, x/columns
                                t1 = (last_decision_point[1] - grid[1])**2
                                #second term, y/rows
                                t2 = (last_decision_point[0] - grid[0])**2
                                final_distance = sqrt(t1 + t2)
                                #This could overwrite if multiple moves are the same distance
                                #We'll take that chance for now and maybe improve later
                                distances[final_distance] = grid
                            #Find the one that gets us closer
                            sorted_distances = distances.keys()
                            sorted_distances.sort()
                            our_move = distances[sorted_distances[0]]
                            
                        move_direction = "SC"
                        #Update last_moves to remove our shortcut
                        self.past_moves = self.past_moves[:self.past_moves.index(our_move)]
                        
                        print "[Move %s] FOUND SHORTCUT! [PAST_MOVES: %s]" % (self.context.total_moves, len(self.past_moves))
            
            #Failed to find shortcut, backtrack
            if our_move is None:
                if self.backtracking is False:
                    print "[Move %s] BACKTRACKING [PAST_MOVES: %s]..." % (self.context.total_moves, len(self.past_moves))
                self.backtracking = True
                move_direction = "BT"
                try:
                    our_move = self.past_moves.pop(-1)
                except:
                    print "[Move %s] BACKTRACKING FAILED - GRID UNSOLVABLE"
        #We have a blue or white move, append our current grid to the past moves.
        else:
            self.past_moves.append(self.snake.current_grid)
        
        #Blue moves first, then white.
        if len(blue_blocks) > 0:
            if self.backtracking is True:
                print "[Move %s] SEEKING [PAST_MOVES: %s]..." % (self.context.total_moves, len(self.past_moves))
            self.backtracking = False
            our_move = blue_blocks.pop(0) #Take the first one
            move_direction = our_move[1]
            our_move = our_move[0][0]
        elif len(white_blocks) > 0:
            if self.backtracking is True:
                print "[Move %s] SEEKING [PAST_MOVES: %s]..." % (self.context.total_moves, len(self.past_moves))
            self.backtracking = False
            #Pick first choice given to us if its the start or we can't continue on in the same direction as before
            if self.snake.direction == "START" or white_blocks.has_key(self.snake.direction) is False:
                move_direction = white_blocks.keys()[0]
                our_move = white_blocks[move_direction][0]
            else:
                our_move = white_blocks[self.snake.direction][0]
                move_direction = self.snake.direction
            del(white_blocks[move_direction])
        
        
        #If there are any other white or blue block moves we add them to current_grid's list in self.decision_points
        if len(white_blocks) > 0:
            if self.decision_points.has_key(self.snake.current_grid) is False:
                self.decision_points[self.snake.current_grid] = []
            for direction, grid in white_blocks.iteritems():
                self.decision_points[self.snake.current_grid].append(grid[0])
        if len(blue_blocks) > 0:
            if self.decision_points.has_key(self.snake.current_grid) is False:
                self.decision_points[self.snake.current_grid] = []
            for grid in blue_blocks:
                self.decision_points[self.snake.current_grid].append(grid[0][0])
                
        #Similarly, remove our current move from the list of decision_points if it exists
        for decision_point, grid_list in self.decision_points.iteritems():
            if our_move in grid_list:
                self.decision_points[decision_point].pop(grid_list.index(our_move))
                #If that was the last move for this decision point, remove it from the dict
                if len(self.decision_points[decision_point]) == 0:
                    del(self.decision_points[decision_point])
        
        #Make our move and update our direction of travel
        self.snake.direction = move_direction
        self.snake.moveSnake(our_move)



    #Helper functions for pathfinder
    def hl_move(self, grid):
        old_grid_item = self.snake.game_grid.item(*self.last_hl_grid)
        new_grid_item = self.snake.game_grid.item(*grid)
        new_grid_item.setBackground(self.snake.grid_item_states[5])
        old_grid_item.setBackground(self.snake.grid_item_states[0])
        self.last_hl_grid = grid

    def go_to_last_decision_point(self):
        #Pull the last decision point.
        if len(self.decision_points) > 0:
            #We must remember to reinsert this data later if there are still more decision points
            dp_grid, dpoints = self.decision_points.pop(0)
#            print "%s Going back to previous decision point at %s..." % (str(self.snake.current_grid), dp_grid)
            #Cut our current path chain just after that point
            try:
                dp_grid_index = self.current_path_chain.index(dp_grid)
            except:
                print "==================================="
                print "this error again..."
                print self.current_path_chain
                print self.decision_points
                print self.snake.current_grid
                print dp_grid
                self.quitting = True
                print "-------------------------------------"
                return
            self.current_path_chain = self.current_path_chain[:dp_grid_index+1]
            #Take the next decision point or closer if metric is enabled
            if self.metric is True:
                #For brevity's sake
                g2 = self.snake.context.finish_grid
                self.snake_direction = sorted(dpoints.items(), key=lambda (_,g1): sqrt(( (g2[0]-g1[0])**2 )+( (g2[1]-g1[1])**2) ))[0][0]
                self.snake.current_grid = dpoints.pop(self.snake_direction)
            else:
                self.snake_direction, self.snake.current_grid = dpoints.popitem()
            #Reinsert the data if there are still more decision points
            if len(dpoints) > 0:
                self.decision_points.insert(0, (dp_grid, dpoints))
            else:
                #If this was the last possible move in this decision point we go back one step with our safe bookmark
                if len(self.decision_points) > 0:
                    self.last_decision_point = self.decision_points[0]
            return True
        else:
            print "%s No more decision points, hit the end." % str(self.snake.current_grid)
            return False
    #Only for start-to-finish grids
    #Metric=True will use follow the path that gets closer to the finish
    #hl mode will show where the algo is currently at by highlighting its current grid
    #This slows down the search considerably however
    def pathfinder_1(self, metric=False, hlmode=False):
        self.snake_direction = "START"
        self.successful_paths = []
        self.current_path_chain = []
        self.decision_points = []
        self.max_chain_length = 1000 #How long before we just stop searching this main branch?
        self.last_decision_point = None
        self.last_hl_grid = self.snake.current_grid
        self.metric = metric

        print "%s Testing possible paths..." % str(self.snake.current_grid)

        while self.quitting is False:
            self.current_path_chain.append(self.snake.current_grid)
            raw_possible_moves = self.snake.getMoves()
            white_blocks = {}
            finish_blocks = {}

            if len(self.current_path_chain) > self.max_chain_length:
                if self.go_to_last_decision_point() is True:
                    continue
                else:
                    break

            for direction, move in raw_possible_moves.iteritems():
                if move[0] is not None:
                    if move[0] in self.current_path_chain:
                        continue
                    #Is this the finish?
                    if move[1] == 6:
                        finish_blocks[direction] = move[0]

                    elif move[1] == 0:
                        white_blocks[direction] = move[0]

            #Remove moves that reverse our direction
            if len(self.current_path_chain)> 0 and len(white_blocks) > 0:
                for direction, grid in white_blocks.iteritems():
                    if grid == self.current_path_chain[-1]:
                        del(white_blocks[direction])
                        break


            #We hit a dead end (wall or our own path)
            #We just go back to the last decision point and explore that
            if (len(white_blocks) == 0 or len(finish_blocks) > 0):
                #Did we finish at least?
                if len(finish_blocks) > 0:
                    #DONE!
                    self.current_path_chain.append(self.snake.current_grid)
                    self.current_path_chain.append(finish_blocks.values()[0])
                    if self.current_path_chain not in self.successful_paths:
                        #See if its any better than our current path
                        if len(self.successful_paths) > 0 and len(self.current_path_chain) > len(sorted(self.successful_paths, key=lambda path: len(path))[0])-1:
                            pass
                        else:
                            print "%s Found the finish with chain size %s" % (str(self.snake.current_grid), len(self.current_path_chain)-1)
                            self.successful_paths.append(self.current_path_chain)
                            #Set a bookmark here as we branch out to find shorter paths
                            if len(self.decision_points) > 0:
                                self.last_decision_point = self.decision_points[0]
                    else:
                        print "Already found this path? How the heck."
#                else:
#                    print "%s Hit a dead end!" % str(self.snake.current_grid)

                #now go back to last decision point
                if self.go_to_last_decision_point() is True:
                    continue
                else:
                    break

            #Current path exceeds smallest successful path (if there is one)
            elif len(self.successful_paths) > 0 and len(self.current_path_chain) >= len(sorted(self.successful_paths, key=lambda path: len(path))[0])-1:
                #print "Current chain length longer than previously successful chains. Stopping search in this branch."
                #Need to delete all decision points made since our last bookmark
                if len(self.decision_points) > 0 and self.last_decision_point in self.decision_points:
                    last_dp_index = self.decision_points.index(self.last_decision_point)
                    self.decision_points = self.decision_points[last_dp_index:]
                if self.go_to_last_decision_point() is True:
                    continue
                else:
                    break

            elif metric is True:
                g2 = self.snake.finish_grid
                self.snake_direction = sorted(white_blocks.items(), key=lambda (_,g1): sqrt(( (g2[0]-g1[0])**2 )+( (g2[1]-g1[1])**2) ))[0][0]

            #Starting off or hit a wall
            elif self.snake_direction == "START" or white_blocks.has_key(self.snake_direction) is False:
                self.snake_direction = white_blocks.keys()[0] # Could instead pull the val that is in our intended direction
#                print "%s Changing direction to %s" % (str(self.snake.current_grid), self.snake_direction)


            our_move = white_blocks.pop(self.snake_direction)

            #if we have any excess possible move choices we create a decision point
            if len(white_blocks) > 0:
                dp = white_blocks #Might need to copy instead of assign. We'll see how it goes.
                self.decision_points.insert(0, (self.snake.current_grid, dp))

            self.snake.current_grid = our_move

            #If we haven't found the finish, keep setting a bookmark
            if len(self.successful_paths) == 0 and len(self.decision_points) > 0:
                self.last_decision_point = self.decision_points[0]

            if hlmode:
                self.hl_move(our_move)
                sleep(float(TICKRATE_MS/float(1000)))



        if len(self.successful_paths) > 0:
            if hlmode: self.hl_move(self.snake.current_grid)
            shortest_path = sorted(self.successful_paths, key=lambda chain: len(chain))[0]
            self.snake.current_grid = shortest_path.pop(0)

            print "Done searching paths, found %s paths total." % len(self.successful_paths)
            print "Shortest path was %s in length. Running that path now..." % len(shortest_path)
            self.quitting = False
            for grid in shortest_path:
                if self.quitting is True:
                    print "Quit called"
                    break
                self.snake.moveSnake(grid)
                Qt.QApplication.processEvents()
                sleep(float(TICKRATE_MS/float(1000)))
        else:
            print "Could not find any solutions to the finish starting from %s" % str(self.snake.start_grid)

        print "Pathfinder Finished!"


    def a_star(self):
        #number of paths to test each round
        SAMPLE_SIZE = 5
        #Going to use a reverse singly linked list with these grid objects
        class Grid(object):
            def __init__(gself, coords, prev=None):
                gself.coords = coords
                gself.prev = prev
                #Estimate our path cost: f(x) = g(x) + h(x)
                #Shortest distance to finish from this grid: h(x)
                distance = sqrt( ((gself.coords[0]-self.snake.finish_grid[0])**2) + ((gself.coords[1]-self.snake.finish_grid[1])**2) )
                gself.cost = gself.getLength() + distance
            def __eq__(gself, othergrid):
                if isinstance(othergrid, Grid):
                    if othergrid.coords == gself.coords: return True
                    else: return False
                elif isinstance(othergrid, tuple):
                    if othergrid == gself.coords: return True
                    else: return False
            def extend(gself, newgridcoords):
                return Grid(newgridcoords, prev=gself)
            def getLength(gself):
                length = 1
                prev = gself.prev
                while prev is not None:
                    prev = prev.prev
                    length += 1
                return length
            #Wrapper around Snake.getMoves() to make the code cleaner
            def getMoves(gself):
                #We dont care about the direction or grid type, just the coords and filter out 'None' moves
                self.snake.current_grid = gself.coords
                return [grid for grid, _ in self.snake.getMoves().values() if grid is not None]


        fringe_set = []
        explored_set = []
        finish_set = []
        start_grid = Grid(self.snake.start_grid)
        finish_grid = Grid(self.snake.finish_grid)

        #Populate our set of possible path chains from the start grid
        fringe_set = [start_grid]
        #Loop through our fringe_set until empty and extend the top SAMPLE_SIZE sets with the lowest path cost
        while len(fringe_set) > 0 and self.quitting is False:
            fringe_set = sorted(fringe_set, key=lambda path: path.cost)
            #Slice off the lowest SAMPLE_SIZE # of sets
            test_set = fringe_set[:SAMPLE_SIZE]
            fringe_set = fringe_set[SAMPLE_SIZE:]

            for testgrid in test_set:
                if self.quitting is True:
                    break

                #Add this grid's possible moves to the fringe set if we haven't explored them already
                for coords in testgrid.getMoves():
                    if coords in explored_set or coords in fringe_set:
                        continue
                    newgrid = Grid(coords, prev=testgrid)
                    #check if this path is worse than any solutions we currently have
                    if len(finish_set) > 0 and newgrid.cost > sorted(finish_set, key=lambda p: p.getLength())[0].cost:
                        continue
                    if coords == finish_grid.coords:
                        finish_set.append(newgrid)
                        finish_length = newgrid.getLength()-1
                        print "Found finish at size %s" % finish_length
                        #Filter our any fringe path ends that are already longer than this successful path
                        fringe_set = list(filter(lambda p: p.getLength() < finish_length, fringe_set))
                    else:
                        fringe_set.append(newgrid)

                explored_set.append(testgrid)


        #A* is finished! Lets show the shortest successful path if we have one.
        if len(finish_set) > 0:
            shortest_path_end_node = sorted(finish_set, key=lambda path: path.getLength())[0]
            shortest_path = [shortest_path_end_node.coords]
            prev = shortest_path_end_node.prev
            while prev is not None:
                shortest_path.insert(0, prev.coords)
                prev = prev.prev
            self.snake.current_grid = shortest_path.pop(0)
            print "A* Finished! Found %s complete paths after exploring %s grids (Efficiency rating with shortest path (%s long): %.2f%%)!" % (len(finish_set), len(explored_set), len(shortest_path), (float(len(shortest_path))/len(explored_set))*100)
            print "Running the shortest path now"
            self.quitting = False
            for grid in shortest_path:
                if self.quitting is True:
                    print "Quit called"
                    break
                self.snake.moveSnake(grid)
                Qt.QApplication.processEvents()
                sleep(float(TICKRATE_MS/float(1000)))
        else:
            print "A* Could not find any solutions to the finish starting from %s" % str(self.snake.start_grid)


        
        

class Snake(object):
    def __init__(self, start_grid, grid_item_states, game_grid, grid_item_tracker, context):
        self.start_grid = start_grid
        self.finish_grid = context.finish_grid
        self.current_grid = start_grid
        self.game_grid = game_grid
        self.grid_item_tracker = grid_item_tracker
        self.grid_item_states = grid_item_states
        self.collected_objectives = 0
        self.found_all = False
        self.found_finish = False
        self.context = context
        self.direction = "NOTUSED"
    
    def getMoves(self):
        #this function returns all available moves
        #Only support up down left and right for now, no diagonal.
        moves = {}
        
        try:
            upgrid = (self.current_grid[0]-1, self.current_grid[1])
            moves["up"] = [upgrid, self.grid_item_tracker[upgrid]]
            if moves["up"][1] == 2: #Roadblock
                moves["up"] = [None, None]
        except:
            moves["up"] = [None, None]
        try:
            downgrid = (self.current_grid[0]+1, self.current_grid[1])
            moves["down"] = [downgrid, self.grid_item_tracker[downgrid]]
            if moves["down"][1] == 2: #Roadblock
                moves["down"] = [None, None]
        except:
            moves["down"] = [None, None]
        try:
            leftgrid = (self.current_grid[0], self.current_grid[1]-1)
            moves["left"] = [leftgrid, self.grid_item_tracker[leftgrid]]
            if moves["left"][1] == 2: #Roadblock
                moves["left"] = [None, None]
        except:
            moves["left"] = [None, None]
        try:
            rightgrid = (self.current_grid[0], self.current_grid[1]+1)
            moves["right"] = [rightgrid, self.grid_item_tracker[rightgrid]]
            if moves["right"][1] == 2: #Roadblock
                moves["right"] = [None, None]
        except:
            moves["right"] = [None, None]
            
        return moves
        
    
    def moveSnake(self, new_grid):
        #Check if we found an objective
        if self.grid_item_tracker[new_grid] == 1:
            self.foundObjective()
            
        #check if we found the finish
        elif self.grid_item_tracker[new_grid] == 6:
            self.foundFinish()
        
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
        print "[Move %s] FOUND OBJ!" % str(self.context.total_moves+1)
        self.collected_objectives += 1
        self.context.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">%s/%s</span></p></body></html>" % (self.collected_objectives, self.context.total_objectives))
        if self.collected_objectives == self.context.total_objectives:
            self.found_all = True
            
    def foundFinish(self):
        print "[Move %s] FOUND FINISH!" % str(self.context.total_moves+1)
        self.found_finish = True
        
        
    
class uiFunctions(object):
    def __init__(self, MW_ref):
        self.MW = MW_ref
        self.game_instance_thread = None
        self.grid_item_tracker = {}
        self.grid_item_states = {}
        self.objective_grids = [] #So we don't have to search for them every time set the finish grid and have to reset them all
        self.grid_locked = False
        self.grid_size = (25, 36)
        self.start_grid = None
        self.finish_grid = None
        self.clock_timer = 0
        self.total_objectives = 0
        self.total_moves = 0
        self.loadstate = None
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
        #finish
        self.grid_item_states[6] = QtGui.QBrush(QtGui.QColor(168, 0, 255, 255))
        #snake tail color
        self.grid_item_states[7] = QtGui.QBrush(QtGui.QColor(40, 150, 0, 255))
    
    def updateClock(self):
        self.clock_timer += 1
        minutes = self.clock_timer/60
        seconds = self.clock_timer%60
        self.MW.time_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">%02d:%02d</span></p></body></html>" % (minutes, seconds))
    
    
    #Non-reverable for now. For the snake minigame
    def invertGridColors(self):
        self.grid_item_states[0] = QtGui.QBrush(QtGui.QColor(0, 0, 0, 255))
        #In the future it is simple to just to a XOR operation on the color value to obtain its inverse (255->0 and vice-versa)
    
    
    def incrementMoveCount(self):
        #Increment move count
        self.total_moves += 1
        self.MW.moves_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">%s</span></p></body></html>" % self.total_moves)
    
    def unlockGrid(self):
        self.grid_locked = False
        self.MW.stop_button.setEnabled(False)
        self.MW.start_button.setEnabled(True)
    
    def resetGrid(self, is_reload=False, minigame_override=False):
        #Stop any current run
        if minigame_override is False:
            try:
                self.stopButtonPressed(quiet=True)
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
        self.finish_grid = None
        #Reset time, found, and moves count to zero
        self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/0</span></p></body></html>")
        self.MW.time_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">00:00</span></p></body></html>")
        self.MW.moves_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#000000;\">0</span></p></body></html>")
        self.clock_timer = 0
        self.total_objectives = 0
        self.objective_grids = []
        self.total_moves = 0
        self.loadstate = None
        #Finally unlock the grid
        if minigame_override is False:
            self.unlockGrid()
        
        #Yeah this is lazy, but meh
        if is_reload is False:
            self.MW.MainWindow.setWindowTitle("Algosnake :: Blank Grid")
    
    
    
    def setGridItem(self, grid, new_mode, init_mode=False):
        new_start_grid_item = self.MW.game_grid.item(*grid)
        
        if init_mode is False:
            #Check for old mode, otherwise mode is 0
            if self.grid_item_tracker.has_key(grid) is False:
                old_grid_mode = 0
            else:
                old_grid_mode = self.grid_item_tracker[grid]
            #Decrement objective if it was set
            if old_grid_mode == 1 and grid in self.objective_grids:
                self.total_objectives -= 1
                self.objective_grids.remove(grid)
                self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/%s</span></p></body></html>" % self.total_objectives)
            
            #Reset start position
            elif old_grid_mode == 3:
                self.start_grid = None
                
            #reset finish position
            elif old_grid_mode == 6:
                self.finish_grid = None

        #increment new objective
        if new_mode == 1:
            self.total_objectives += 1
            self.objective_grids.append(grid)
            self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/%s</span></p></body></html>" % self.total_objectives)
            #Reset the finish grid if its been set. We can't have both objectives and the finish grid set at once.
            if self.finish_grid is not None:
                self.setGridItem(self.finish_grid, 0)
            
            
        #Setting new start position
        elif new_mode == 3:
            #reset old start grid if necessary
            if self.start_grid is not None:
                old_start_grid_item = self.MW.game_grid.item(*self.start_grid)
                old_start_grid_item.setBackground(self.grid_item_states[0])
                self.grid_item_tracker[self.start_grid] = 0
            #set new start grid
            self.start_grid = (grid[0], grid[1])
        
        #Setting new finish position
        elif new_mode == 6:
            #Reset the old finish grid if its set
            if self.finish_grid is not None:
                old_finish_grid_item = self.MW.game_grid.item(*self.finish_grid)
                old_finish_grid_item.setBackground(self.grid_item_states[0])
                self.grid_item_tracker[self.finish_grid] = 0
            #Reset any objectives if they have been set
            if self.total_objectives > 0:
                for obj_grid in self.objective_grids:
                    #Would recurse but it only resets half of them when I do lol
                    old_obj_grid_item = self.MW.game_grid.item(*obj_grid)
                    old_obj_grid_item.setBackground(self.grid_item_states[0])
                    self.grid_item_tracker[obj_grid] = 0
                    self.total_objectives -= 1
                self.total_objectives = 0
                self.objective_grids = []
                self.MW.num_found_indicator.setText("<html><head/><body><p align=\"center\"><span style=\" font-size:16pt; font-weight:600; color:#ff0000;\">0/0</span></p></body></html>")
            
            self.finish_grid = (grid[0], grid[1])
        
        
        #Finally update tracker and update new item background
        self.grid_item_tracker[(grid[0], grid[1])] = new_mode
        new_start_grid_item.setBackground(self.grid_item_states[new_mode])
    
    
    def itemClicked(self, row, column):
        print "(%s, %s)" % (row, column)
        if self.grid_locked == True:
            return
        
        self.loadstate = None
        
        qapp = QtGui.QApplication.instance()
        keyboard_mods = qapp.queryKeyboardModifiers()
        #holding control key to set start grid
        if keyboard_mods == QtCore.Qt.ControlModifier:
            self.setGridItem((row, column), 3)
        #Holding shift sets a roadblock
        elif keyboard_mods == QtCore.Qt.ShiftModifier:
            self.setGridItem((row, column), 2)
        #Holding control and shift sets finish position
        elif keyboard_mods == QtCore.Qt.ShiftModifier | QtCore.Qt.ControlModifier:
            self.setGridItem((row, column), 6)
        #Normal click
        else:   
            #Toggle straight to off from all blocks
            if self.grid_item_tracker[(row,column)] >= 1:
                self.setGridItem((row, column), 0)
            else:
                self.setGridItem((row, column), 1)
    
    def startButtonPressed(self):
        self.updateSpeed()
        self.lock_controls(True)
        snake_instance = Snake(self.start_grid, self.grid_item_states, self.MW.game_grid, self.grid_item_tracker, self)
        if self.game_instance_thread is not None and self.game_instance_thread.isAlive():
            self.game_instance_thread.join()
        self.game_instance_thread = RunInstance(snake_instance, self)
        self.game_instance_thread.start()
        self.grid_locked = True

        
        if self.loadstate is None:
            self.setLoadState()
    
    def stopButtonPressed(self, quiet=False):
        self.game_instance_thread.quitting = True
        self.start_grid = self.game_instance_thread.snake.current_grid
        self.grid_item_tracker[self.game_instance_thread.snake.current_grid] = 3
        self.lock_controls(False)
        if quiet == False:
            print "ROUND STOPPED"
    
    def lock_controls(self, locked):
        self.MW.stop_button.setEnabled(locked)
        self.MW.start_button.setDisabled(locked)
        self.MW.reset_button.setDisabled(locked)
        self.MW.clear_button.setDisabled(locked)
        #self.MW.speed_selector.setDisabled(locked)
        self.MW.algoList.setDisabled(locked)

    def setLoadState(self):
        self.loadstate = {}
        self.loadstate["start_grid"] = self.start_grid
        self.loadstate["game_item_tracker"] = DC(self.grid_item_tracker)
    
    def stopAndQuit(self):
        try:
            self.stopButtonPressed()
        except:
            pass
        self.MW.MainWindow.close()
    
    def updateSpeed(self):
        global TICKRATE_MS
        #Figure out speed
        #            Low speeds 1-10              High speeds 11-19                  Super high speeds 20-28
        speeds = [x for x in range(1000, 0, -100)] + [x for x in range(90, 0, -10)] + [x for x in range(9, 0, -1)]
        TICKRATE_MS = speeds[self.MW.speed_selector.value()-1]
        
    
    def fileDialogMaster(self, main_mode, file_mode, dialog_caption, filters="Algosnake Grid (*.gridstate)"):
        start_dir = os.getcwd()
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
    #We can save a LOT of space in our .gridstate files by not saving default squares (white blocks) and instead assuming any missing
    #blocks are white blocks. That way we only save the blue, red, green, and purple blocks. That should cut down on the size of the smaller
    #gridstates by a ton.
    def saveGrid(self):
        savefilepath = self.fileDialogMaster(QtGui.QFileDialog.AcceptSave, QtGui.QFileDialog.AnyFile, "Save Current Grid...")
        
        if len(savefilepath) > 0:
            #We only want grids that arent mode 0
            tmp_grid_item_tracker = {} 
            for grid, mode in self.grid_item_tracker.iteritems():
                if mode != 0:
                    tmp_grid_item_tracker[grid] = mode
            
            savedata = [tmp_grid_item_tracker, self.start_grid]
            savedata = cPickle.dumps(savedata)
            
            with open(savefilepath, "w") as savefile:
                savefile.write(savedata)
            
            #GGC will probably do this anyway but im paranoid
            del(tmp_grid_item_tracker)
        
        self.setLoadState()
    
    def reloadGrid(self):
        try:
            self.stopButtonPressed()
        except:
            pass
        
        if self.loadstate is None:
            return
        #make a copy of the loadstate and then reset everything
        loadstate = DC(self.loadstate)
        self.resetGrid(is_reload=True)
        self.start_grid = loadstate["start_grid"]
        self.total_objectives = 0
        #Load the grid
        for grid, mode in loadstate["game_item_tracker"].iteritems():
            if grid is None: continue
            #change any explored boxes to unexplored
            if mode == 5:
                mode = 0
            self.setGridItem(grid, mode, init_mode=True)
        
        self.setLoadState()
        #Unlock the grid
        self.grid_locked = False
            
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
        self.total_objectives = 0
        
        #Since we can't know which grids are set and which aren't we won't loop through the loaded grid_item_tracker
        #Instead we just loop over the known bounds of the grid and look inside grid_item_tracker for corresponding data.
        for x, y in itertools_product(range(self.grid_size[0] + 1), range(self.grid_size[1] + 1)):
            #Check if our grid is in the grid_item_tracker, if not create a default entry
            if (x, y) in self.grid_item_tracker.keys():
                self.setGridItem((x, y), self.grid_item_tracker[(x,y)], init_mode=True)
            else:
                self.grid_item_tracker[(x,y)] = 0
            
        
        self.MW.MainWindow.setWindowTitle("Algosnake :: %s" % loadfilepath)
        self.setLoadState()
