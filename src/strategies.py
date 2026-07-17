def candidates(sudoku, i, j):

    if sudoku[i][j] != 0:
        return []

    possibles = []

    for value in range(1, 10):
        if possibleValue(sudoku, i, j, value):
            possibles.append(value)

    return possibles

def nakedSingles(sudoku):
    counter=0
    modification = False

    for i in range(9):
        for j in range(9):

            if sudoku[i][j] == 0:

                cadidate_list = candidates(sudoku, i, j)

                if len(cadidate_list) == 1:
                    sudoku[i][j] = cadidate_list[0]
                    modification = True
                    counter+=1

    return modification,counter