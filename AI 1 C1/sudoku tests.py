import numpy as np
import time as t


veLPath = "/home/bitchass/Documents/Homework/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/very_easy_puzzle.npy"
eLPath = "/home/bitchass/Documents/Homework/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/easy_puzzle.npy"
mLPath = "/home/bitchass/Documents/Homework/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/medium_puzzle.npy"
hLPath = "/home/bitchass/Documents/Homework/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/hard_puzzle.npy"
veSLPath = "/home/bitchass/Documents/Homework/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/very_easy_solution.npy"
eSLPath = "/home/bitchass/Documents/Homework/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/easy_solution.npy"
mSLPath = "/home/bitchass/Documents/Homework/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/medium_solution.npy"
hSLPath = "/home/bitchass/Documents/Homework/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/hard_solution.npy"

vePath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/very_easy_puzzle.npy"
ePath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/easy_puzzle.npy"
mPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/medium_puzzle.npy"
hPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/hard_puzzle.npy"
veSPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/very_easy_solution.npy"
eSPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/easy_solution.npy"
mSPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/medium_solution.npy"
hSPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/hard_solution.npy"

"""
    Input
        sudoku : 9x9 numpy array; empty = 0
    Output
        Solution if available or all -1 if there's no solution
"""

# CODE environment

"""
important notes:
constraints applied? 324 of them
- 81 row
- 81 column
- 81 square
- 81 number

and... 729 placements for the numbers. goodness.
so 324 columns, 729 rows.

"""

class Node: # so this'll just be a 1 or 0. it will connect to its column, to its column, to whatever's... man this is so strange
    def __init__ (self):
        self.l = self.r = self.u = self.d = self # they all point to themselves. will need to implement this somehow
        self.header = None # this will belong to a column, a constraint
        self.row = None # this is gonna be a pain in the arse.

    # def newConnect(self, one, two, three, four): # L R U D
    #     self.l = one if one != None else self
    #     self.r = two if two != None else self
    #     self.u = three if three != None else self
    #     self.d = four if four != None else self
    
    # def reconnect(self):
    #     self.l.r = self
    #     self.r.l = self
    #     self.u.d = self
    #     self.d.u = self

    # def disconnect(self):
    #     self.l.r = self.r
    #     self.r.l = self.l
    #     self.u.d = self.d
    #     self.d.u = self.u

    def hrztCover(self): 
        self.l.r = self.r
        self.r.l = self.l
    def vertCover(self):
        self.u.d = self.d
        self.d.u = self.u
    def hrztUncover(self):
        self.l.r = self
        self.r.l = self
    def vertUncover(self):
        self.u.d = self
        self.d.u = self
        


class ColumnN(Node): 
    def __init__ (self, colName):
        super().__init__()
        self.colName = colName
        self.length = 0
        self.header = self # just points to itself until it has a 1 in itself, i think.
    
    # a column is the exact same as every other node, so you don't have to worry about changing anything, however
    # in KAX, there's tons of partial solutions nad backtracking going on, so for the majority of the time 
    # the idea of columns being fully covered and uncovered all the time's an important aspect to include
    # so these functions will be implemented now:
    def fullDisconnect (self): # algorithm x related
        # cover!
        self.hrztCover()
        i = self.d
        while i != self:
            j = self.r
            while j != i: 
                j.vertCover()
                j.header.length -= 1
                j = j.r
            i = i.d
    def fullConnect (self): # algorithm x related
        # uncover!
        i = self.u
        while i != self:
            j = self.l
            while j != i: 
                j.header.length += 1
                j.vertUncover()
                j = j.l
            i = i.u

        self.hrztUncover() # nothing has to be done here as the relation of course still exists
        
class DLX:
    def __init__(self, columns):
        self.cRHeader = ColumnN("ROOT") # stores the root. cR = control row. wording has been used to minimise confusion between words between classes
        self.cRCols = {} # stores columns

        for n in columns:
            tempCol = ColumnN(n)
            self.cRCols[n] = tempCol

            tempCol.r = self.cRHeader
            tempCol.l = self.cRHeader.left
            
            self.cRHeader.l.r = tempCol
            self.cRHeader.l = tempCol

# class RowH(Node):
#     def __init__ (self, rowName):
#         super().__init__()
#         self.row = rowName


"""
possible naming convention for column headers:
1nm <- 1 = Row Constraint, N = Row, M = Number
2nm <- 2 = Col... same as above
3nm <- 3 = Square... same as above
4nm <- 4 = Exact cell, 

"""

def sudoku_solver(sudoku):
    unsolvable = False # unsolvability can only be determined in two manners for sudoku: more than one solution found / poorly designed clues
    universe = {1,2,3,4,5,6,7,8,9} # each cell's given a subset of the universe. the whole point of the search will hopefully be erasing
    clues = 0 # this is a clue tracker, there's a neat little trick where if there are any less than 17 clues, the sudoku is immediately 'unsolvable'
    
    
    return None

# raise NotImplementedError()

# CHECKING environment:
sudoku = np.load(vePath)
# solutions = np.load(veSPath)
# print()
# print("First sudoku:")
# print(sudoku[0], "\n")
# print("Solution of first sudoku:")
# print(solutions[0])

startTime = t.process_time()
sudoku_solver(sudoku[0])
endTime = t.process_time()

