FILE_NAME = "input.txt"
position = 50
counter = 0


def parse_input(line, position, counter):
    dir = line[0]
    move = int(line[1:])

    position += move if dir == "R" else -move
    position = position % 100

    if position == 0:
        counter += 1
    return position, counter


with open(FILE_NAME) as f:
    data = f.readlines()

    for line in data:
        position, counter = parse_input(line, position, counter)

    print(f"Final position: {position}")
    print(f"Number of times position 0 was reached: {counter}")
