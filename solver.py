# Sodoku Puzzle Solver by Hunter McGee
# Uses backtracking to recursively find a solution by filling all open squares (denoted by 0)
# If no possible solution, then No solution is output.
# If a solution is found, the solved puzzle is output.

myBoard = [
    [0, 0, 0, 0, 0, 6, 0, 7, 0],
    [0, 7, 0, 9, 0, 4, 0, 3, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 1],
    [3, 0, 6, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 8, 0, 1, 9, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 5],
    [1, 0, 0, 0, 0, 0, 0, 0, 7],
    [0, 3, 0, 5, 0, 8, 0, 9, 0],
    [0, 5, 0, 4, 0, 0, 0, 0, 0],
]

def solve(board):
    nextEmpty = firstEmpty(board)

    if not nextEmpty: # Base case, no more open spaces (SOLVED)
        return True
    else:
        row, col = nextEmpty

    for guess in range(1, 10):
        if validate(board, (row, col), guess):
            board[row][col] = guess

            if solve(board):
                return True

            board[row][col] = 0 # guess doesn't work


def validate(board, pos, value):
    row = pos[0]
    col = pos[1]

    #Check all numbers in row
    for j in range(len(board[0])):
        if board[row][j] == value and col != j:
            return False
    #Check all numbers in col
    for i in range(len(board)):
        if board[i][col] == value and row != i:
            return False
    #Check all numbers in square
    squareX = col // 3
    squareY = row // 3

    for j in range(squareX * 3, squareX * 3 + 3):
        for i in range(squareY * 3, squareY * 3 + 3):
            if board[i][j] == value and (i, j) != (row, col):
                return False
    return True

def firstEmpty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j) # row, col
    return None

def printBoard(board):
    for i in range(len(board)):
        if i != 0 and i % 3 == 0:
            print("_ _ _ _ _ _ _ _ _ _ _ _")

        for j in range(len(board[0])):
            if j != 0 and j % 3 == 0:
                print(" | ", end="")

            if j == (len(board[0]) - 1): # last element in row
                print(board[i][j])
            else:
                print(board[i][j], end=" ")

printBoard(myBoard)
print("\n")

solution = solve(myBoard)

if solution:
    printBoard(myBoard)
else:
    print("No Solution.")