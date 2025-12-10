import math

FILE_NAME = 'input.txt'


def total_sum(lines, operators):
    ops = {'+': sum, '*': math.prod}
    columns = zip(*lines)
    return sum(ops[op](col) for col, op in zip(columns, operators))

with open(FILE_NAME, 'r') as file:
    lines = file.readlines()
    numbers = []
    for line in lines[:-1]:
        numbers_line = ([int(num) for num in line.split()])
        numbers.append(numbers_line)
    operators = lines[-1].strip().split()

    sum = total_sum(numbers, operators)
    print(sum) # 4387670995909
