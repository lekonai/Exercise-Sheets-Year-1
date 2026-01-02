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
- 81 (has) number

and... 729 placements for the numbers.
so 324 columns, and up to ... 576 possible placements? if given minimum amount of clues (17)

"""

class Node: # so this'll just be a 1 or 0. it will connect to its column, to its column, to whatever's... man this is so strange
    def __init__ (self):
        self.l = self.r = self.u = self.d = self # they all point to themselves. will need to implement this somehow
        self.header = None # this will belong to a column, a constraint
        self.row = None # this is gonna be a pain in the arse.
    def hrztCover(self): # the fact cover is remove and uncover is add feels weird goodness
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
            j = i.r
            while j != i: 
                j.vertCover()
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
                j.vertUncover()
                j = j.l
            i = i.u
        self.hrztUncover() # nothing has to be done here as the relation of course still exists
        
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
        nodesToLink = [] # to link later
        for c in colConns:
            curCol = self.cRCols[c] # seek dictionary
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
        if self.cRHeader.r == self.cRHeader: # this is when a solution's reached, ideally
            return solution[:] # why doesn't pass by value exist 
        
        curCol = self.mrvHeuristic()
        if curCol.length == 0:
            return None # break out
        
        curCol.fullDisconnect()

        curRow = curCol.d
        while curRow != curCol:
            solution.append(curRow.row) # get the names, will have to reencode properly but this is easiest way of getting all IDs

            coverNodes = curRow.r
            while coverNodes != curRow:
                coverNodes.header.fullDisconnect()
                coverNodes = coverNodes.r
            
            nextSolution = self.KAX(solution)
            if nextSolution != None:
                curCol.fullConnect()
                return nextSolution # reattach and then proceed with the next call
            
            # this is the back tracking step: if we end up in an unrecoverable spot we just uncover again and the call stack breaks up until there's 
            # a "next solution"
            uncoverNodes = curRow.l
            while uncoverNodes != curRow:
                uncoverNodes.header.fullConnect()
                uncoverNodes = uncoverNodes.l 
            
            solution.pop() # partial solution is approved so remove it
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
                trueRow = row + 1 # actual one indexed
                trueCol = col + 1 # don't forget that its zero indexed but you're handling it as one indexed
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
                    for i in range (1,10):
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
        endSolved = np.zeros((9,9))
        for p in solved:
            converted = str(p)
            # print(converted) # debug
            endSolved[int(converted[1]) - 1][int(converted[2]) - 1] = int(converted[0])
        return endSolved

    solvedEncoded = encode(solvedUnencoded)

    print(solvedEncoded) # debug
    # print(solved) # debug
    # print("done") # debug
    return solvedEncoded

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
print(endTime - startTime)
