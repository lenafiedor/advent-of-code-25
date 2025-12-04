FILE_NAME = 'input.txt'
sum = 0

def max_jolt(line):
    sum = 0
    current_index = 0

    for i in range(12):
        max_num = (max(line[current_index:len(line)-(11-i)]))
        current_index += line[current_index:].index(max_num) + 1
        sum += int(max_num) * (10 ** (11 - i))

    return sum

with open(FILE_NAME) as f:
    lines = f.readlines()
    for line in lines:
        sum += max_jolt(line.strip())

    print(f'Sum: {sum}')
