FIlE_NAME = 'input.txt'
grid = []

def is_accessible(grid, row, index):
    count = 0
    row_trimmed = max(0, row - 1), min(len(grid) - 1, row + 1)
    index_trimmed = max(0, index - 1), min(len(grid[row]) - 1, index + 1)

    for r in range(row_trimmed[0], row_trimmed[1] + 1):
        for i in range(index_trimmed[0], index_trimmed[1] + 1):
            if grid[r][i] == '@' or grid[r][i] == 'x':
                count += 1
    count -= 1  # Exclude the current position
    return count < 4

def count_rolls(grid):
    count = 0
    has_any_accessible = True

    while has_any_accessible:
        has_any_accessible = False
        for i, row in enumerate(grid):
            for j, char in enumerate(row):
                if char == '@' and is_accessible(grid, i, j):
                    has_any_accessible = True
                    count += 1
                    grid[i] = grid[i][:j] + 'x' + grid[i][j+1:]
        
        for i, row in enumerate(grid):
            grid[i] = row.replace('x', '.')
    return count, grid

with open(FIlE_NAME, 'r') as file:
    for line in file.readlines():
        grid.append(line.strip())

rolls, grid = count_rolls(grid)
print(f'Number of accessible rolls: {rolls}')
