import re

FIlE_NAME = 'input.txt'
grid = []

def is_accessible(grid, row, index):
    count = 0
    row_trimmed = max(0, row - 1), min(len(grid) - 1, row + 1)
    index_trimmed = max(0, index - 1), min(len(grid[row]) - 1, index + 1)

    for r in range(row_trimmed[0], row_trimmed[1] + 1):
        for i in range(index_trimmed[0], index_trimmed[1] + 1):
            if grid[r][i] == '@':
                count += 1
    count -= 1  # Exclude the current position
    return count < 4

def count_rolls(grid):
    count = 0
    for i in range(len(grid)):
        for j, char in enumerate(grid[i]):
            if char == '@' and is_accessible(grid, i, j):
                count += 1
    return count

with open(FIlE_NAME, 'r') as file:
    for line in file.readlines():
        grid.append(line.strip())

rolls = count_rolls(grid)
print(f'Number of accessible rolls: {rolls}')
