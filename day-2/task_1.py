import re

FILE_NAME = 'input.txt'

def find_patterns(rng):
    sum = 0
    for num in range(rng[0], rng[1] + 1):
        pattern = r'^(\d+)\1$'
        result = re.match(pattern, str(num))
        if result:
            sum += num

    return sum


with open(FILE_NAME) as f:
    ranges = f.read().strip().split(',')
    ranges_num = [list(map(int, r.split('-'))) for r in ranges]
    sum = 0

    for r in ranges_num:
       sum += find_patterns(r)
    print(f"Sum: {sum}")
