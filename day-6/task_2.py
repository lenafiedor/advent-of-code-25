import math

FILE_NAME = 'input.txt'


def parse_lines(lines: list[str]) -> list[list[int]]:

    columns = list(zip(*lines))
    numbers = []
    current_group = []
    current_num = None

    for col in columns:
        digits = [c for c in col if c.isdigit()]

        if digits:
            for d in digits:
                current_num = (current_num or 0) * 10 + int(d)
            current_group.append(current_num)
            current_num = None
        elif all(c == ' ' for c in col):
            numbers.append(current_group)
            current_group = []

    if current_num is not None:
        current_group.append(current_num)
    if current_group:
        numbers.append(current_group)

    return numbers

def calculate_sum(numbers: list[list[int]], operators: list[str]) -> int:
    ops = {'+': sum, '*': math.prod}
    return sum(ops[op](nums) for nums, op in zip(numbers, operators))


with open(FILE_NAME, 'r') as file:
    lines = file.readlines()
    numbers = parse_lines(lines[:-1])
    operators = lines[-1].strip().split()

    total_sum = calculate_sum(numbers, operators)
    print(total_sum) # 9625320374409
