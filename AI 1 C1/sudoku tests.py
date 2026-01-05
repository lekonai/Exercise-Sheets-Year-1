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

import numpy as np
import time as t

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
- 81 (has) number

and... 729 placements for the numbers.
so 324 columns, and up to ... 576 possible placements? if given minimum amount of clues (17)

"""

class Node: # so this'll just be a 1 or 0. it will connect to its column, to its column, to whatever's... man this is so strange
    def __init__ (self):
        self.l = self.r = self.u = self.d = self # they all point to themselves. will need to implement this somehow
        self.header = None # this will belong to a column, a constraint
        self.row = None
    def hrztDisconnect(self): # is cover disconnect?  well not disconnect, but kinda
        self.l.r = self.r
        self.r.l = self.l
    def vertDisconnect(self): # i don't know i think i'll just name my own operations
        self.u.d = self.d
        self.d.u = self.u
    def hrztConnect(self):
        self.l.r = self
        self.r.l = self
    def vertConnect(self):
        self.u.d = self
        self.d.u = self

class ColumnN(Node): 
    def __init__ (self, colName):
        super().__init__()
        self.colName = colName
        self.length = 0
        self.header = self # just points to itself until it has a 1 in itself, i think.
    
    # a column is the exact same as every other node, so you don't have to worry about changing anything
    # though of course to form partial solutions within KAX you must wholly disconnect 
    # without then severing the ACTUAL connection and vice versa
    def fullDisconnect (self): # algorithm x related
        # cover!
        self.hrztDisconnect()
        i = self.d
        while i != self:
            j = i.r
            while j != i: 
                j.vertDisconnect()
                j.header.length -= 1
                j = j.r
            i = i.d

    def fullConnect (self): # algorithm x related
        # uncover!
        i = self.u
        while i != self:
            j = i.l
            while j != i: 
                j.header.length += 1
                j.vertConnect()
                j = j.l
            i = i.u
        self.hrztConnect() # nothing has to be done here as the relation of course still exists
        
class DLX:
    def __init__(self, columns):
        self.cRHeader = ColumnN("ROOT") # stores the root. cR = control row. wording has been used to minimise confusion between words between classes
        self.cRCols = {} # stores columns

        for c in columns:
            tempCol = ColumnN(c)
            self.cRCols[c] = tempCol

            tempCol.r = self.cRHeader
            tempCol.l = self.cRHeader.l # crheader.l shouuuld be either, itself, or the most recently added column node

            self.cRHeader.l.r = tempCol # connect last connected with new addition
            self.cRHeader.l = tempCol # loop root around
    
    def addRow (self, rowN, colConns):
        nodesToLink = []
        for c in colConns:
            curCol = self.cRCols[c] # seek dictionary entry
            curNode = Node()

            curNode.header = curCol
            curNode.row = rowN
            
            # vertical column connection
            curNode.d = curCol
            curNode.u = curCol.u
            curCol.u.d = curNode
            curCol.u = curNode
            curCol.length += 1

            nodesToLink.append(curNode)

        for i in range(len(nodesToLink)):
            nodesToLink[i].r = nodesToLink[(i + 1) % len(nodesToLink)] # linking operation for the nodes on the row
            nodesToLink[i].l = nodesToLink[(i - 1) % len(nodesToLink)] # thank you a level 

    def mrvHeuristic(self): 
        # find column with least rows attached
        minCol = None
        minLength = float('inf')

        curCol = self.cRHeader.r
        while curCol != self.cRHeader:
            if curCol.length < minLength:
                minCol = curCol
                minLength = curCol.length
            curCol = curCol.r
        
        return minCol
    
    def KAX(self, solution):
        # base cases
        if self.cRHeader.r == self.cRHeader: 
            return solution[:] # why doesn't pass by value exist 
        
        curCol = self.mrvHeuristic()
        if curCol.length == 0:
            return None # break out, nothing in front
        
        curCol.fullDisconnect()

        curRow = curCol.d
        while curRow != curCol:
            solution.append(curRow.row) # dont forget to reencode

            coverNodes = curRow.r
            while coverNodes != curRow:
                coverNodes.header.fullDisconnect()
                coverNodes = coverNodes.r
            
            nextSolution = self.KAX(solution)
            if nextSolution != None:
                curCol.fullConnect()
                return nextSolution # reattach and then proceed with the next call
            
            # back tracking step: if we end up in an unrecoverable spot we return nothing,
            # the call stack goes one back and we just uncover again and the it continues to break up
            # up until there's a "next solution"
            uncoverNodes = curRow.l
            while uncoverNodes != curRow:
                uncoverNodes.header.fullConnect()
                uncoverNodes = uncoverNodes.l 
            
            solution.pop()
            curRow = curRow.d
        curCol.fullConnect()
        return None

"""
possible naming convention for column headers:
1nm <- 1 = Row Constraint, N = Row, M = Number
2nm <- 2 = Col... same as above
3nm <- 3 = Square... same as above 
4nm <- 4 = Fill, m = cell location, does it have a number?

row naming convention:
nMiMj = n is the number, (mi, mj) is the cell location. these are placements, every single one will have to have at least 4 1s.

"""

def sudoku_solver(sudoku):
    totalColumns = []
    for i in range (111,200):
        if i % 10 != 0:
            totalColumns.append(i)
            totalColumns.append(i + 100)
            totalColumns.append(i + 200)
            totalColumns.append(i + 300)
    totalColumns.sort()
    mainMatrix = DLX(totalColumns)
    for row in range(9):
        for col in range(9):
                trueRow = row + 1 
                trueCol = col + 1 
                box = ((row // 3) * 3 + (col // 3)) + 1
                num = sudoku[row][col]
                if num != 0:
                    rowName = (f"{num}" + f"{trueRow}" + f"{trueCol}")
                    # print(f"inputting {rowName}") # debug
                    rowConstraintCol = f"1{trueRow}{num}"
                    colConstraintCol = f"2{trueCol}{num}"
                    squareConstraintCol = f"3{box}{num}"
                    fillConstraintCol = f"4{trueRow}{trueCol}"
                    mainMatrix.addRow(int(rowName), [int(rowConstraintCol), int(colConstraintCol), int(squareConstraintCol), int(fillConstraintCol)])
                else:
                    for i in range (1,10): # all possible placements, definitely could be optimised, but the algorthim's quick enough anyway
                        num = i 
                        rowName = (f"{num}" + f"{trueRow}" + f"{trueCol}")
                        # print(f"inputting {rowName}") # debug
                        rowConstraintCol = f"1{trueRow}{num}"
                        colConstraintCol = f"2{trueCol}{num}"
                        squareConstraintCol = f"3{box}{num}"
                        fillConstraintCol = f"4{trueRow}{trueCol}"
                        mainMatrix.addRow(int(rowName), [int(rowConstraintCol), int(colConstraintCol), int(squareConstraintCol), int(fillConstraintCol)])
    
    # print("pre solve") # debug
    # print(mainMatrix.cRCols.keys())
    solvedUnencoded = mainMatrix.KAX([])
    # solved.sort() # only here for debug
    
    def encode(solved):
        if solved == None:
            return np.full((9,9), -1, np.int8)
        else:
            endSolved = np.zeros((9,9), np.int8)
            for p in solved:
                converted = str(p)
                # print(converted) # debug
                endSolved[int(converted[1]) - 1][int(converted[2]) - 1] = int(converted[0])
            return endSolved

    solvedEncoded = encode(solvedUnencoded)

    # print(solvedEncoded) # debug
    # print(solved) # debug
    # print("done") # debug
    return solvedEncoded

# raise NotImplementedError()

# CHECKING environment:
sudoku = np.load(veLPath)
sudoku1 = np.load(eLPath)
sudoku2 = np.load(mLPath)
sudoku3 = np.load(hLPath)
# solutions = np.load(veSPath)
# print()
# print("First sudoku:")
# print(sudoku[0], "\n")
# print("Solution of first sudoku:")
# print(solutions[0])

totalTime = 0

for i in range(len(sudoku)):
    startTime = t.process_time()
    sudoku_solver(sudoku[i])
    endTime = t.process_time()
    print(endTime - startTime)
    totalTime += (endTime - startTime)

for i in range(len(sudoku1)):
    startTime = t.process_time()
    sudoku_solver(sudoku1[i])
    endTime = t.process_time()
    print(endTime - startTime)
    totalTime += (endTime - startTime)

for i in range(len(sudoku2)):
    startTime = t.process_time()
    sudoku_solver(sudoku2[i])
    endTime = t.process_time()
    print(endTime - startTime)
    totalTime += (endTime - startTime)

for i in range(len(sudoku3)):
    startTime = t.process_time()
    sudoku_solver(sudoku3[i])
    endTime = t.process_time()
    print(endTime - startTime)
    totalTime += (endTime - startTime)

print(f"total time: {totalTime}")