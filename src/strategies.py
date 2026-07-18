def update_neighbors(candidates, i, j, val):
    for k in range(9):
        candidates[i][k].discard(val) # Fila
        candidates[k][j].discard(val) # Columna
    
    # 3x3
    bi, bj = (i // 3) * 3, (j // 3) * 3
    for r in range(bi, bi + 3):       
        for c in range(bj, bj + 3):   
            candidates[r][c].discard(val)

def create_candidates(sudoku):
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
    return modified

def next_sudoku(sudoku):
    candidates_matrix = create_candidates(sudoku) 
    while True:

        modified_naked, _ = naked_single(sudoku, candidates_matrix)
        modified_hidden = hidden_single(sudoku, candidates_matrix)
        
        if modified_naked or modified_hidden:
            continue
        else:
            break