def solverSudoku(sudoku):
    for i in range(0,9): 
        for j in range(0,9):
            if sudoku[i][j]==0: 
                for value in range(1,10):
                    if possibleValue(sudoku, i, j, value):
                        sudoku[i][j]=value
                        if solverSudoku(sudoku)==True: 
                            return True
                        sudoku[i][j]=0
                return False
    return True



def possibleValue(sudoku,i, j, value):
    for k in range(0,9):    
        if sudoku[i][k]==value or sudoku[k][j]==value:
            return False
    if squareCheck(sudoku,i,j,value)==False: return False
    return True


def squareCheck(sudoku,i,j,value):
    r = i//3*3
    c = j//3*3
    for l in range(0,3):
        for m in range(0,3):
            if sudoku[r+l][c+m]==value:
                return False
    return True