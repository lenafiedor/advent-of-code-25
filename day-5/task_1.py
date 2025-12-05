FILE_NAME = 'input.txt'


def is_in_range(start, end, number):
    return int(start) <= int(number) <= int(end)

def check_numbers(ranges, numbers):
    result = []
    for number in numbers:
        found = False
        for r in ranges:
            start, end = r.split('-')
            if is_in_range(start, end, number):
                found = True
                break
        result.append(found)
    return result

with open(FILE_NAME, 'r') as f:
    content = f.read()

    part1, part2 = content.split('\n\n')

    ranges = part1.strip().split('\n')
    numbers = part2.strip().split('\n')

    numbers_in_range = check_numbers(ranges, numbers)
    print(f'Numbers found: {sum(numbers_in_range)}')
