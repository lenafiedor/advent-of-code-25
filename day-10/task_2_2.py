from __future__ import annotations
from typing import List, Tuple
import pulp

FILE_NAME = "input.txt"


def parse_input(file_name: str):
    diagrams = []
    buttons = []
    joltages = []
    with open(file_name, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            diagrams.append(parts[0].strip("[]"))  # ignored for joltage mode

            btns = []
            for tok in parts[1:-1]:
                inside = tok.strip("()")
                if inside == "":
                    btns.append(tuple())
                else:
                    btns.append(tuple(int(x) for x in inside.split(",")))
            buttons.append(btns)

            jol = parts[-1].strip("{}")
            if jol == "":
                joltages.append([])
            else:
                joltages.append([int(x) for x in jol.split(",")])
    return diagrams, buttons, joltages


def min_presses_joltage_milp(buttons: List[Tuple[int, ...]], target: List[int]) -> int:
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

    # normalize buttons to valid indices and drop empty ones (they can never help)
    btns = []
    for b in buttons:
        b2 = tuple(i for i in b if 0 <= i < k)
        if b2:
            btns.append(b2)
    if not btns:
        raise ValueError("No usable buttons for non-zero target.")

    m = len(btns)

    # Build MILP
    prob = pulp.LpProblem("joltage", pulp.LpMinimize)

    x = [pulp.LpVariable(f"x{j}", lowBound=0, cat=pulp.LpInteger) for j in range(m)]
    prob += pulp.lpSum(x)  # objective: minimize total presses

    # Constraints per counter
    for i in range(k):
        prob += pulp.lpSum(x[j] for j in range(m) if i in btns[j]) == target[i], f"c{i}"

    # Solve
    # msg=0 -> silent. Set to 1 if you want solver logs.
    status = prob.solve(pulp.PULP_CBC_CMD(msg=0))

    if pulp.LpStatus[status] != "Optimal":
        raise ValueError(f"No optimal solution found; status={pulp.LpStatus[status]}")

    return int(pulp.value(prob.objective))


if __name__ == "__main__":
    _diagrams, buttons, joltages = parse_input(FILE_NAME)

    total = 0
    for idx, (btns, tgt) in enumerate(zip(buttons, joltages), start=1):
        presses = min_presses_joltage_milp(btns, tgt)
        print(f"Machine {idx}: min joltage presses = {presses}")
        total += presses

    print("TOTAL min presses (joltage mode):", total)
