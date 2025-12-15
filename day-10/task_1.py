from typing import List, Tuple
from utils import *

FILE_NAME = 'input.txt'


def build_solution(reduced_rows: List[Tuple[int, int]], where: List[int], m: int) -> Tuple[int, List[int], List[int]]:
    """
    Given a reduced GF(2) system:
        reduced_rows: list of (row_mask, rhs) after elimination (RREF-style)
        where[col] = pivot_row index if col is pivot, else -1
        m: number of variables/buttons

    Returns:
        x0: particular solution as an m-bit int (free vars = 0)
        basis: list of m-bit ints, one for each free variable
        free_cols: list of free column indices (same order as basis)
    """

    free_cols = [c for c in range(m) if where[c] == -1]

    x0 = 0
    for col in range(m):
        r = where[col]
        if r != -1:
            rhs = reduced_rows[r][1] & 1
            if rhs:
                x0 |= (1 << col)

    basis: List[int] = []
    for f in free_cols:
        v = 1 << f
        for col in range(m):
            r = where[col]
            if r != -1:
                row_mask, _rhs = reduced_rows[r]
                if (row_mask >> f) & 1:
                    v |= (1 << col)

        basis.append(v)

    return x0, basis, free_cols


def min_weight_solution(x0: int, basis: List[int]) -> Tuple[int, int]:
    """
    Enumerate all solutions x = x0 XOR (subset of basis) and return:
        (min_presses, best_x)
    Best when k=len(basis) is reasonably small (<= ~25-30).
    """
    k = len(basis)
    best_presses = x0.bit_count()
    best_x = x0

    for mask in range(1 << k):
        x = x0
        for i in range(k):
            if (mask >> i) & 1:
                x ^= basis[i]

        presses = x.bit_count()
        if presses < best_presses:
            best_presses = presses
            best_x = x
            if best_presses == 0:
                break

    return best_presses, best_x


if __name__ == '__main__':
    diagrams, buttons, _ = parse_input(FILE_NAME)
    total_sum = 0

    for machine_idx, (diagram_str, button_tuples) in enumerate(zip(diagrams, buttons), start=1):
        n = len(diagram_str)
        target = diagram_to_bitmask(diagram_str)
        btn_masks = [button_to_bitmask(b) for b in button_tuples]

        rows = build_rows(n, target, btn_masks)
        reduced, where, rank, bad = gaussian_elimination(rows, m=len(btn_masks))
        if bad:
            raise ValueError("No solution for this machine")

        x0, basis, free_cols = build_solution(reduced, where, m=len(btn_masks))
        min_presses, best_x = min_weight_solution(x0, basis)
        total_sum += min_presses
    
    print("Total sum of min presses over all machines =", total_sum) # 507
