from typing import List, Tuple

Point = Tuple[int, int]
FILE_NAME = "input.txt"


def area(p1: Point, p2: Point) -> int:
    x1, y1 = p1
    x2, y2 = p2
    return (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)


def tile_pairs(points: List[Point]):
    n = len(points)
    for i in range(n):
        p1 = points[i]
        for j in range(i + 1, n):
            yield p1, points[j]


def get_edges(points: List[Point]):
    n = len(points)
    edges = []
    for i in range(n):
        a = points[i]
        b = points[(i + 1) % n]
        edges.append((a, b))
    return edges


def edge_crosses_rectangle(
    edge: Tuple[Point, Point],
    rect: Tuple[Point, Point],
) -> bool:
    (ex1, ey1), (ex2, ey2) = edge
    (rx1, ry1), (rx2, ry2) = rect

    if ex1 == ex2:
        x = ex1
        ey_min = min(ey1, ey2)
        ey_max = max(ey1, ey2)
        ry_min = min(ry1, ry2)
        ry_max = max(ry1, ry2)

        if rx1 <= rx2:
            between = (x > rx1) and (x < rx2)
        else:
            between = (x > rx2) and (x < rx1)

        if ey_min <= ry_min:
            overlap = ey_max > ry_min
        else:
            overlap = ry_max > ey_min

        return between and overlap

    else:
        y = ey1
        ex_min = min(ex1, ex2)
        ex_max = max(ex1, ex2)
        rx_min = min(rx1, rx2)
        rx_max = max(rx1, rx2)

        if ry1 <= ry2:
            between = (y > ry1) and (y < ry2)
        else:
            between = (y > ry2) and (y < ry1)

        if ex_min <= rx_min:
            overlap = ex_max > rx_min
        else:
            overlap = rx_max > ex_min

        return between and overlap


def rectangle_valid(rect: Tuple[Point, Point], edges) -> bool:
    for e in edges:
        if edge_crosses_rectangle(e, rect):
            return False
    return True


def largest_rectangle(points: List[Point]) -> Tuple[Tuple[Point, Point] | None, int]:
    edges = get_edges(points)
    best_area = 0
    best_rect = None

    pairs = list(tile_pairs(points))
    for (p1, p2) in pairs:
        x1, y1 = p1
        x2, y2 = p2
        if x1 == x2 or y1 == y2:
            continue

        rect = (p1, p2)

        if rectangle_valid(rect, edges):
            a = area(p1, p2)
            if a > best_area:
                best_area = a
                best_rect = rect

    return best_rect, best_area


if __name__ == '__main__':
    with open(FILE_NAME, 'r') as f:
        points = [tuple(map(int, line.strip().split(","))) for line in f if line.strip()]
    rect, a = largest_rectangle(points)
    print(f"Largest rectangle: {rect}")
    print(f"Area: {a}")
