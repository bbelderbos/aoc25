import argparse
from pathlib import Path
from math import prod


def solve_part1(data: str) -> int:
    lines = data.splitlines()
    grid = [[int(x) for x in line.split()] for line in lines[:-1]]
    grid_transposed = list(zip(*grid))
    ops = lines[-1].split()
    return sum(
        prod(nums) if o == "*" else sum(nums) for o, nums in zip(ops, grid_transposed)
    )


def solve_part2(data: str) -> int:
    lines = data.splitlines()
    max_width = max(len(line) for line in lines)
    grid = [line.ljust(max_width) for line in lines]
    grid_transposed = list(zip(*grid))
    total = 0
    current = []
    # need to go in reverse order to collect numbers first
    # before hitting the operator
    for col in reversed(grid_transposed):
        num = "".join(col[:-1]).strip()
        if not num:
            continue
        current.append(int(num))
        op = col[-1].strip()
        # we hit the operator, so process and reset current
        if op in ("*", "+"):
            total += prod(current) if op == "*" else sum(current)
            current = []
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    part1_result = solve_part1(input_text)
    print(f"Part 1: {part1_result}")
    assert part1_result == 4412382293768

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 7858808482092


if __name__ == "__main__":
    main()
