from itertools import combinations
from math import prod


FILE_NAME = 'input.txt'
NUM = 1000


def calculate_distance(point1, point2):
    return ((point1[0] - point2[0]) ** 2 + 
            (point1[1] - point2[1]) ** 2 + 
            (point1[2] - point2[2]) ** 2) ** 0.5, point1, point2

def smallest_distance(coords):
    return min(calculate_distance(p1, p2) for p1, p2 in combinations(coords, 2))

def find_top_n(coords, n):
    circuits = []
    connections = sorted(combinations(coords, 2), key=lambda pair: calculate_distance(pair[0], pair[1])[0])

    for i in range(n):
        point1, point2 = connections[0]
        connections.pop(0)
        loc_p1, loc_p2 = None, None

        for j, c in enumerate(circuits):
            if point1 in c and point2 not in c:
                loc_p1 = j
            elif point2 in c and point1 not in c:
                loc_p2 = j
            elif point1 in c and point2 in c:
                loc_p1, loc_p2 = j, j
                break
        
        if loc_p1 is not None and loc_p2 is not None and loc_p1 != loc_p2:
            circuits[loc_p1].extend(circuits[loc_p2])
            del circuits[loc_p2]
        elif loc_p1 is not None and loc_p1 == loc_p2:
            pass
        elif loc_p1 is not None:
            circuits[loc_p1].append(point2)
        elif loc_p2 is not None:
            circuits[loc_p2].append(point1)
        else:
            circuits.append([point1, point2])

    return prod(len(c) for c in sorted(circuits, key=len, reverse=True)[:3])    


with open(FILE_NAME, 'r') as file:
    lines = file.readlines()
    coords = [(int(line.split(',')[0]), int(line.split(',')[1]), int(line.split(',')[2])) for line in lines]
    result = find_top_n(coords, NUM)
    print(f'Result: {result}') # 79560
