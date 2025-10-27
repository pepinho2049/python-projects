
def find_next_empty(puzzle):
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r,c
            else: 
                return None, None #if no space in the grid are empty

def is_valid(puzzle, guess, row, col):
    row_vals = puzzle[row]
    if guess in row_vals:
        return False # we check whether the guess is in the row
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False # we guess whether the guess in the column
    
    #for checking the 3x3 square
    
    row_start = (row//3) * 3
    col_start = (col // 3) * 3
    
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

def solve_sudoku(puzzle):
    row, col = find_next_empty(puzzle)
    if row is None:
        return True
    for guess in range(1,10):
        if is_valid(puzzle, guess, row, col):
            puzzle[row][col] = guess
            if solve_sudoku(puzzle):
                return True
            
        puzzle[row][col] = -1 #resetting the value
        
    return False
