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
constraints applied?
- row
- column
- square

"""

class Cell:
    domain = {1, 2, 3, 4, 5, 6, 7, 8, 9}
    def __init__ (self, row, column):
        self.row = row
        self.column = column
        self.square = 
    def location (self):
        print(f"{self.row}, {self.column}")
def sudoku_solver(sudoku):
    unsolvable = False # unsolvability can only be determined in two manners for sudoku: more than one solution found / poorly designed clues
    universe = {1,2,3,4,5,6,7,8,9} # each cell's given a subset of the universe. the whole point of the search will hopefully be erasing
    clues = 0 # this is a clue tracker, there's a neat little trick where if there are any less than 17 clues, the sudoku is immediately 'unsolvable'

    exploreMatrix = [[],[],[],[],[],[],[],[],[]]
    for i in range(9):
        for j in range(9):
            temp = Cell(i + 1, j + 1)
            temp.location()
            exploreMatrix.insert(i, temp)

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

