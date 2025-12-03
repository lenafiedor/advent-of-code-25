FILE_NAME = "input.txt"
position = 50
counter = 0


def parse_input(line, position, counter):
    dir = line[0]
    move = int(line[1:])

    print(f"Move: {line.strip()} | Current position: {position} | Current counter: {counter}")

    if dir == "R":
        new_position = position + move
        counter += new_position // 100
        print(f"Counter increased by {(position + move) // 100}, new counter: {counter}")
    elif dir == "L":
        new_position = position - move
        if new_position == 0:
            counter += 1
        if new_position < 0:
            if position != 0:
                counter += 1
            counter += (move - position) // 100

    new_position = new_position % 100

    print("Position after mod 100:", new_position)
    print()

    return new_position, counter

with open(FILE_NAME) as f:
    data = f.readlines()

    for line in data:
        position, counter = parse_input(line, position, counter)

    print("=="*20)
    print(f"Final position: {position}")
    print(f"Number of times position 0 was reached: {counter}")
