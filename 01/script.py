import argparse
from pathlib import Path


DIAL_SIZE = 100
START = 50


def step(pos: int, rot: str, amount: int) -> int:
    delta = amount if rot == "R" else -amount
    return (pos + delta) % DIAL_SIZE


def solve_part1(data: str) -> int:
    pos, pw = START, 0
    for row in data.splitlines():
        rot, num = row[0], int(row[1:])
        pos = step(pos, rot, num)
        if pos == 0:
            pw += 1
    return pw


def solve_part2(data: str) -> int:
    pos, pw = START, 0
    for row in data.splitlines():
        rot, num = row[0], int(row[1:])
        for _ in range(num):
            pos = step(pos, rot, 1)
            if pos == 0:
                pw += 1
    return pw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    part1_result = solve_part1(input_text)
    print(f"Part 1: {part1_result}")
    assert part1_result == 1055

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 6386


if __name__ == "__main__":
    main()
