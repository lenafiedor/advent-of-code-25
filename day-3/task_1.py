FILE_NAME = 'input.txt'
sum = 0

def max_jolt(line):
    first = max(line[:len(line)-1])
    second = max(line[line.index(first)+1:])

    # print(f"First max: {first}, Second max: {second}")
    return int(first)*10 + int(second)

with open(FILE_NAME) as f:
    lines = f.readlines()
    for line in lines:
        sum += max_jolt(line.strip())

    print(f"Sum: {sum}")
