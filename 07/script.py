import argparse
from collections import Counter
from pathlib import Path


def load_grid(data: str) -> list[list[str]]:
    return [list(line.strip()) for line in data.splitlines()]


def find_char_in_row(row: list[str], char: str) -> int:
    try:
        return row.index(char)
    except ValueError:
        raise ValueError(f"Character {char!r} not found in row") from None


def solve(data: str, part2: bool = False) -> int:
    grid = load_grid(data)
    start_col = find_char_in_row(grid[0], "S")

    beams = Counter({start_col: 1})
    total_splits = 0

    for row in grid[1:]:
        new_beams = Counter()
        for col, n in beams.items():
            if row[col] == "^":
                total_splits += 1
                for nc in (col - 1, col + 1):
                    new_beams[nc] += n
            else:
                new_beams[col] += n
        beams = new_beams
    return sum(beams.values()) if part2 else total_splits


def solve_part1(data: str) -> int:
    return solve(data)


def solve_part2(data: str) -> int:
    return solve(data, part2=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    part1_result = solve_part1(input_text)
    print(f"Part 1: {part1_result}")
    assert part1_result == 1651

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 108924003331749


if __name__ == "__main__":
    main()
