FILE_NAME = 'input.txt'

def sum_splits(board):
    sum = 0
    for i in range(1, len(board)):
        for j in range(len(board[i])):
            if board[i][j] == '^' and board[i-1][j] == '|':
                board[i] = board[i][:j - 1] + '|' + board[i][j:]
                board[i] = board[i][:j + 1] + '|' + board[i][j + 2:]
                sum += 1
            elif board[i-1][j] == '|' or board[i-1][j] == 'S':
                board[i] = board[i][:j] + '|' + board[i][j + 1:]
            
    return sum



with open(FILE_NAME, 'r') as file:
    lines = file.readlines()
    sum = sum_splits(lines)
    print(f'Sum of splits: {sum}')
