import numpy as np
import time as t
import math

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
possible naming convention for column headers:

"""

class Cell:
    def __init__(self, row, col, val, bClue):
        
        self.row = row
        self.col = col
        self.val = val
        self.isClue = bClue
        self.domain = {1,2,3,4,5,6,7,8,9} if bClue == False else {int(val)}
        # self.square = 

    def returnX(self):
        return self.row
    
    def returnY(self):
        return self.col
    
    def returnSquare(self):
        return self.square

    def isClue(self):
        return self.isClue
    
    def returnValue(self):
        return self.val
    
    def returnDomain(self):
        return self.domain
    
def sudoku_solver(sudoku):
    unsolvable = False # unsolvability can only be determined in two manners for sudoku: more than one solution found / poorly designed clues
    universe = {1,2,3,4,5,6,7,8,9} # each cell's given a subset of the universe. the whole point of the search will hopefully be erasing
    clues = 0 # this is a clue tracker, there's a neat little trick where if there are any less than 17 clues, the sudoku is immediately 'unsolvable'

    def createMatrix(sudoku, clues):
        matrix = []
        for x in range(9):
            tempList = []
            for y in range(9):
                curCell = Cell(x + 1, y + 1, sudoku[x][y], (False if sudoku[x][y] == 0 else True))
                if sudoku[x][y] != 0:
                    clues += 1
                tempList.append(curCell)
            matrix.append(tempList)
        return matrix, clues
    
    def validateByRow(matrix, row):
        pass
    def validateByColumn(matrix, rowmatrix, column):
        pass
    def validateBySquare(matrix, row, column):
        pass

    objectMatrix, clues = createMatrix(sudoku, clues)

    # def constraintPropagation():
    #     pass


    for x in range(9):
        for y in range(9):
            print(objectMatrix[x][y].returnSquare(), end=" ")
        print("\n")

    # if clues < 17:
    #     return 

    return None

# raise NotImplementedError()

# CHECKING environment:
sudoku = np.load(vePath)
# solutions = np.load(veSPath)
# print()
# print("First sudoku:")
print(sudoku[0], "\n")
# print("Solution of first sudoku:")
# print(solutions[0])

startTime = t.process_time()
sudoku_solver(sudoku[0])
endTime = t.process_time()
