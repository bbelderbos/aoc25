# /// script
# dependencies = [
#   "PuLP",
# ]
# ///
import argparse
from itertools import combinations
from pathlib import Path

import pulp  # type: ignore


def solve_machine(machine: str) -> int:
    lights, *tokens = machine.split()
    lights = lights.strip("[]")
    buttons = [
        tuple(map(int, t.strip("()").split(","))) for t in tokens if t.startswith("(")
    ]

    initial = list(lights)
    m = len(buttons)

    for n in range(m + 1):  # 0 .. m presses
        for idxs in combinations(range(m), n):
            state = initial[:]
            for i in idxs:
                for pos in buttons[i]:
                    state[pos] = "#" if state[pos] == "." else "."
            if all(c == "." for c in state):
                return n
    raise ValueError("No solution found")


def solve_part1(data: str) -> int:
    return sum(solve_machine(machine) for machine in data.splitlines())


def build_A(buttons: list[tuple[int, ...]], target: list[int]) -> list[list[int]]:
    L, B = len(target), len(buttons)
    A = [[0] * B for _ in range(L)]
    for j, btn in enumerate(buttons):
        for i in btn:
            A[i][j] = 1
    return A


def min_presses_ilp(machine: str) -> int:
    lights, *tokens, target_str = machine.split()

    buttons = [tuple(map(int, t.strip("()").split(","))) for t in tokens]
    target = list(map(int, target_str.strip("{}").split(",")))

    A = build_A(buttons, target)
    L, B = len(target), len(buttons)

    prob = pulp.LpProblem("machine", pulp.LpMinimize)

    # integer vars x_j >= 0
    x = [pulp.LpVariable(f"x_{j}", lowBound=0, cat="Integer") for j in range(B)]

    # objective: min sum_j x_j
    prob += pulp.lpSum(x)

    # constraints: for each counter i, sum_j A[i][j] * x_j == target[i]
    for i in range(L):
        prob += pulp.lpSum(A[i][j] * x[j] for j in range(B)) == target[i]

    # solve
    prob.solve(pulp.PULP_CBC_CMD(msg=False))

    if pulp.LpStatus[prob.status] != "Optimal":
        raise ValueError("No optimal ILP solution")

    return int(sum(v.value() for v in x))


def solve_part2(data: str) -> int:
    return sum(min_presses_ilp(machine) for machine in data.splitlines())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    part1_result = solve_part1(input_text)
    print(f"Part 1: {part1_result}")
    assert part1_result == 441

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 18559


if __name__ == "__main__":
    main()
