import copy

def update_neighbors(candidates, i, j, val):
    """Updates the candidates of the i row, j column and 3x3 box 
    for the value val that has been just added to the sudoku"""

    for k in range(9):
        candidates[i][k].discard(val) # Fila
        candidates[k][j].discard(val) # Columna
    
    # 3x3
    bi, bj = (i // 3) * 3, (j // 3) * 3
    for r in range(bi, bi + 3):       
        for c in range(bj, bj + 3):   
            candidates[r][c].discard(val)

def create_candidates(sudoku):
    """Creates a matrix with the possible numbers for each case"""

    candidates = [[set(range(1, 10)) for value in range(9)] for value in range(9)]
    
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                update_neighbors(candidates, i, j, sudoku[i][j])
                candidates[i][j] = set()
    return candidates


def naked_single(sudoku,candidates_matrix):
    count=0
    modified = False
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0 and len(candidates_matrix[i][j])==1 : 
                val = list(candidates_matrix[i][j])[0]
                sudoku[i][j] = val
                update_neighbors(candidates_matrix, i, j, val)
                candidates_matrix[i][j] = set()
                modified=True
                count+=1
    return modified, count

def hidden_single(sudoku,candidates_matrix):
    count=0
    modified = False
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0: 
                for c in candidates_matrix[i][j]:
                    row_count,col_count,square_count = 0, 0, 0

                    for k in range(9):
                        if c in candidates_matrix[i][k]:
                            row_count += 1
                        if c in candidates_matrix[k][j]:
                            col_count += 1
                    bi, bj = (i // 3) * 3, (j // 3) * 3
                    for ii in range(bi, bi + 3):
                        for jj in range(bj, bj + 3):
                            if c in candidates_matrix[ii][jj]:
                                square_count+=1

                    if row_count == 1 or col_count == 1 or square_count == 1: 
                        sudoku[i][j]=c
                        update_neighbors(candidates_matrix,i,j,c)
                        candidates_matrix[i][j] = set()
                        modified=True
                        count+=1
                        break
    return modified,count

def next_sudoku(sudoku):
    """Updates the sudoku and returns the amount of added numbers by strategy"""

    sudoku_copy = copy.deepcopy(sudoku)
    candidates_matrix=create_candidates(sudoku_copy)

    total_naked_single = 0
    total_hidden_single = 0
   
    
    while True:
        modified_naked, count_n = naked_single(sudoku_copy, candidates_matrix)
        modified_hidden, count_h = hidden_single(sudoku_copy, candidates_matrix)
        
        total_naked_single += count_n
        total_hidden_single += count_h
        
        if not modified_naked and not modified_hidden:
            break
            
    return sudoku_copy, [total_naked_single, total_hidden_single]

def count_empty(sudoku): 
    """Count of empty spaces in the sudoku """

    empty_count=0
    for i in range(9):
        empty_count += sudoku[i].count(0)
    return empty_count

def difficulty_eval(*args): 
    """Returns 
      -(string) Explanation of the difficulty  
      -(int) Level of difficulty from 0 to 1
      """
    
    names=['total_empty','total_naked_singles','total_hidden_singles']
    variables = {}
    for i, total in enumerate(args):
        if i < len(names):
            variables[names[i]]=total

    total_to_fulfill = sum(args)

    if variables["total_naked_singles"]/total_to_fulfill > 0.2 and variables["total_empty"] == 0:
        return "Level: Easy (Naked Singles and Hidden Singles)",0.2
    elif variables["total_naked_singles"]/total_to_fulfill < 0.2 and variables["total_empty"] == 0:
        return "Level: Intermediate (Naked Singles and Hidden Singles)",0.5
    elif variables["total_empty"] == 0:
        return "Level: Hard",0.7
    else:
        return "Level: Not solved",1
    