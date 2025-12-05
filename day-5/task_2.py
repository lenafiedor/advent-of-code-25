FILE_NAME = 'input.txt'


def merge_intervals(intervals):
    intervals.sort()
    stack = []
    stack.append(intervals[0])

    for interval in intervals[1:]:
        if stack[-1][0] <= interval[0] <= stack[-1][-1]:
            stack[-1][-1] = max(stack[-1][-1], interval[-1])
        else:
            stack.append(interval)

    return stack

def is_in_range(start, end, number):
    return int(start) <= int(number) <= int(end)


with open(FILE_NAME, 'r') as f:
    content = f.read()

    ranges = content.split('\n\n')[0].strip().split('\n')
    merged_ranges = merge_intervals([list(map(int, r.split('-'))) for r in ranges])
    sum = sum([end - start + 1 for start, end in merged_ranges])
    print(f'Total numbers in ranges: {sum}')
