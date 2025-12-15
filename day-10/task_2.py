from __future__ import annotations
from typing import List, Tuple
from utils import *
import pulp

FILE_NAME = 'input.txt'


def min_presses_joltage(buttons: List[Tuple[int, ...]], target: List[int]) -> int:
    """
    Exact minimum total presses using MILP:
      minimize sum x_j
      subject to sum_{j: i in btn_j} x_j = target_i for each counter i
      x_j integer >= 0
    """
    k = len(target)
    if k == 0:
        return 0
    if all(v == 0 for v in target):
        return 0

    btns = []
    for b in buttons:
        b2 = tuple(i for i in b if 0 <= i < k)
        if b2:
            btns.append(b2)
    if not btns:
        raise ValueError('No usable buttons for non-zero target.')

    m = len(btns)
    prob = pulp.LpProblem('joltage', pulp.LpMinimize)
    x = [pulp.LpVariable(f'x{j}', lowBound=0, cat=pulp.LpInteger) for j in range(m)]
    prob += pulp.lpSum(x)

    for i in range(k):
        prob += pulp.lpSum(x[j] for j in range(m) if i in btns[j]) == target[i], f'c{i}'

    status = prob.solve(pulp.PULP_CBC_CMD(msg=0))

    if pulp.LpStatus[status] != "Optimal":
        raise ValueError(f'No optimal solution found; status={pulp.LpStatus[status]}')

    return int(pulp.value(prob.objective))


if __name__ == "__main__":
    diagrams, buttons, joltages = parse_input(FILE_NAME)

    total = 0
    for idx, (btns, target) in enumerate(zip(buttons, joltages), start=1):
        print(f'\n=== Machine {idx} ===')
        presses = min_presses_joltage(btns, target)
        print(f'Machine {idx}: min joltage presses = {presses}')
        total += presses

    print('TOTAL min presses (joltage mode):', total) # 18981
