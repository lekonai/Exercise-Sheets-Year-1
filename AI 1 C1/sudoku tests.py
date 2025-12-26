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

# vePath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/very_easy_puzzle.npy"
# ePath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/easy_puzzle.npy"
# mPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/medium_puzzle.npy"
# hPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/hard_puzzle.npy"
# veSPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/very_easy_solution.npy"
# eSPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/easy_solution.npy"
# mSPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/medium_solution.npy"
# hSPath = "C:/Users/Omari/Documents/HOMEWORK AND EDUCATION!/uni/Exercise-Sheets-Year-1/AI 1 C1/sudoku/data/hard_solution.npy"

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

# old code, will delete after next commit:
# class Cell:
#     domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
#     def __init__ (self, row, column, square):
#         self.row = row
#         self.column = column
#         self.square = square

# exploreMatrix = [[],[],[],[],[],[],[],[],[]]
    # for i in sudoku:
    #     for j in sudoku:
    #         temp = Cell(i + 1, j + 1, ((j + 1) // 3) + ((i + 1) // 3))
    #         exploreMatrix.insert(i, temp)
    # print(exploreMatrix)
class Node: # so this'll just be a 1 or 0. it will connect to its column, to its column, to whatever's... man this is so strange
    def __init__ (self):
        self.l = self.r = self.u = self.d = self # they all point to themselves. will need to implement this somehow
        self.header = None # this will belong to a column, a constraint

    def reconnect(self):
        self.l.r = self
        self.r.l = self
        self.u.d = self
        self.d.u = self

    def disconnect(self):
        self.l.r = self.r
        self.r.l = self.l
        self.u.d = self.d
        self.d.u = self.u

class ColumnH(Node): 
    def __init__ (self, colName):
        super().__init__()
        self.column = colName
    def columnName (self):
        print(self.column)
    

class RowH(Node):
    def __init__ (self, rowName):
        super().__init__()
        self.row = rowName


"""
possible naming convention for column headers:

"""

def sudoku_solver(sudoku):
    unsolvable = False # unsolvability can only be determined in two manners for sudoku: more than one solution found / poorly designed clues
    universe = {1,2,3,4,5,6,7,8,9} # each cell's given a subset of the universe. the whole point of the search will hopefully be erasing
    clues = 0 # this is a clue tracker, there's a neat little trick where if there are any less than 17 clues, the sudoku is immediately 'unsolvable'
    
    
    return None

# raise NotImplementedError()

# CHECKING environment:
sudoku = np.load(veLPath)
# solutions = np.load(veSPath)
# print()
# print("First sudoku:")
# print(sudoku[0], "\n")
# print("Solution of first sudoku:")
# print(solutions[0])

startTime = t.process_time()
sudoku_solver(sudoku[0])
endTime = t.process_time()
