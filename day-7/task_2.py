from pathlib import Path

FILE_NAME = "input.txt"


def parse_grid(path: str) -> list[str]:
    text = Path(path).read_text().rstrip("\n")
    return text.splitlines()

def solve(grid: list[str]) -> int:
    height = len(grid)
    width = len(grid[0])

    counts = [0] * width
    counts[grid[0].index("S")] = 1

    for r in range(1, height):
        row = grid[r]
        new = [0] * width

        for c, n in enumerate(counts):
            if n == 0:
                continue
            if row[c] == "^":
                if c > 0:
                    new[c - 1] += n
                if c + 1 < width:
                    new[c + 1] += n
            else:
                new[c] += n

        counts = new

    return sum(counts)


if __name__ == "__main__":
    grid = parse_grid(FILE_NAME)
    timelines = solve(grid)
    print("Number of timelines:", timelines) # 40999072541589
