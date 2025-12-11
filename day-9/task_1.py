from itertools import combinations

FILE_NAME = 'input.txt'


def calculate_area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

def find_largest(tiles):
    return max(calculate_area(p1, p2) for p1, p2 in combinations(tiles, 2))

with open(FILE_NAME, 'r') as file:
    lines = file.readlines()
    red_tiles = [tuple(int(c) for c in line.strip().split(',')) for line in lines]
    largest_area = find_largest(red_tiles)
    print(f'Largest area found: {largest_area}')
