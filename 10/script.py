# /// script
# dependencies = [
#   "z3-solver",
# ]
# ///
import argparse
from itertools import combinations
from pathlib import Path

import z3  # type: ignore


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


def min_presses_ilp(machine: str) -> int:
    lights, *tokens, target_str = machine.split()

    buttons = [tuple(map(int, t.strip("()").split(","))) for t in tokens]
    target = list(map(int, target_str.strip("{}").split(",")))
    o = z3.Optimize()  # optimization context

    vars = z3.Ints(f"n{i}" for i in range(len(buttons)))
    for var in vars:
        o.add(var >= 0)  # x_j ≥ 0

    for i, joltage in enumerate(target):  # one constraint per counter i
        equation = 0
        for b, button in enumerate(buttons):
            if i in button:  # button b touches counter i
                equation += vars[b]  # add x_b to this counter
        o.add(equation == joltage)  # A[i]·x == target[i]

    o.minimize(sum(vars))  # minimize total presses
    o.check()
    return o.model().eval(sum(vars)).as_long()


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
