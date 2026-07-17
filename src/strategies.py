def update_neighbors(candidates, i, j, val):
    for k in range(9):
        candidates[i][k].discard(val) # Row
        candidates[k][j].discard(val) # Column
    
    # 3x3
    bi, bj = (i // 3) * 3, (j // 3) * 3
    for i in range(bi, bi + 3):
        for j in range(bj, bj + 3):
            candidates[i][j].discard(val)

def create_candidates(sudoku):
    candidates = [[set(range(1, 10)) for value in range(9)] for value in range(9)]
    
    for i in range(9):
        for j in range(9):
            if sudoku[i][j] != 0:
                update_neighbors(candidates, i, j, sudoku[i][j])
                candidates[i][j] = set()
    return candidates


def naked_single(sudoku,candidates_matrix):
    modified = False
    for i in range(9):
        for j in range(9):
            if sudoku[i][j]==0 and len(candidates_matrix[i][j])==1 : 
                val = list(candidates_matrix[i][j])[0]
                sudoku[i][j] = val
                update_neighbors(candidates_matrix, i, j, val)
                candidates_matrix[i][j] = set()
                modified=True
    return modified

