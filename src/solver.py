def solver_sudoku(sudoku):
    for i in range(0,9): 
        for j in range(0,9):
            if sudoku[i][j]==0: 
                for value in range(1,10):
                    if possible_value(sudoku, i, j, value):
                        sudoku[i][j]=value
                        if solver_sudoku(sudoku)==True: 
                            return True
                        sudoku[i][j]=0
                return False
    return True



def possible_value(sudoku,i, j, value):
    if sudoku[i][j]!=0:
        return False
    for k in range(0,9):    
        if sudoku[i][k]==value or sudoku[k][j]==value:
            return False
    if square_check(sudoku,i,j,value)==False: return False
    return True


def square_check(sudoku,i,j,value):
    r = i//3*3
    c = j//3*3
    for l in range(0,3):
        for m in range(0,3):
            if sudoku[r+l][c+m]==value:
                return False
    return True