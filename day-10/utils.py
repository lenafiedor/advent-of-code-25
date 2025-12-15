from typing import List, Tuple


def diagram_to_bitmask(diagram: str) -> int:
    bitmask = 0
    for i, char in enumerate(diagram):
        if char == '#':
            bitmask |= (1 << i)
    return bitmask


def button_to_bitmask(button: Tuple[int, ...]) -> int:
    bitmask = 0
    for val in button:
        bitmask |= (1 << val)
    return bitmask


def build_rows(n_lights: int, target_mask: int, button_masks: List[int]) -> List[Tuple[int, int]]:
    rows = []
    m = len(button_masks)
    for i in range(n_lights):
        rm = 0
        for j in range(m):
            if (button_masks[j] >> i) & 1:
                rm |= (1 << j)
        rhs = (target_mask >> i) & 1
        rows.append((rm, rhs))
    
    return rows


def gaussian_elimination(rows: List[Tuple[int, int]], m: int) -> Tuple[List[Tuple[int, int]], List[int], int, bool]:
    """
    Gaussian elimination over GF(2) on an augmented system.

    rows: list of (row_mask, rhs), where
      - row_mask is an m-bit integer (coefficients over buttons/variables)
      - rhs is 0 or 1

    m: number of variables/buttons (number of bits in row_mask)

    Returns:
      reduced_rows: list of (row_mask, rhs) after elimination (modified copy)
      where: list length m, where[col] = pivot_row_index if col is pivot else -1
      rank: number of pivot columns
      inconsistent: True if system has no solution
    """

    a = [(rm, rhs & 1) for (rm, rhs) in rows]
    n = len(a)

    where = [-1] * m
    pivot_row = 0

    for col in range(m):
        sel = -1
        mask = 1 << col
        for r in range(pivot_row, n):
            if a[r][0] & mask:
                sel = r
                break

        if sel == -1:
            continue

        if sel != pivot_row:
            a[pivot_row], a[sel] = a[sel], a[pivot_row]

        where[col] = pivot_row
        pivot_rm, pivot_rhs = a[pivot_row]

        for r in range(n):
            if r == pivot_row:
                continue
            rm, rhs = a[r]
            if rm & mask:
                a[r] = (rm ^ pivot_rm, rhs ^ pivot_rhs)

        pivot_row += 1
        if pivot_row == n:
            break

    rank = pivot_row
    inconsistent = any((rm == 0 and rhs == 1) for (rm, rhs) in a)

    return a, where, rank, inconsistent


def parse_input(file_name: str) -> Tuple[List[str], List[List[Tuple[int, ...]]], List[List[int]]]:
    diagrams = []
    buttons = []
    joltages = []

    with open(file_name, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.split()
            diagrams.append(parts[0].strip('[]'))
            buttons.append([tuple(int(i) for i in parts[i].strip('()').split(',')) for i in range(1, len(parts)-1)])
            joltages.append([int(i) for i in parts[-1].strip('{}').split(',')])
        return diagrams, buttons, joltages
