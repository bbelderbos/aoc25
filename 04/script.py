import argparse
from pathlib import Path
from typing import NamedTuple

ROLL = "@"
MAX_ROLLS_ADJACENT = 4


class Position(NamedTuple):
    x: int
    y: int


DIRECTIONS = [
    Position(-1, -1),
    Position(0, -1),
    Position(1, -1),
    Position(-1, 0),
    Position(1, 0),
    Position(-1, 1),
    Position(0, 1),
    Position(1, 1),
]


def load_grid(data: str) -> dict[Position, str]:
    grid = {}
    for y, line in enumerate(data.splitlines()):
        for x, char in enumerate(line):
            grid[Position(x, y)] = char
    return grid


def get_adjacent_rolls(grid: dict[Position, str], pos: Position) -> int:
    return sum(grid.get(Position(pos.x + d.x, pos.y + d.y)) == ROLL for d in DIRECTIONS)


def solve_part1(data: str) -> int:
    grid = load_grid(data)
    return sum(
        char == ROLL and get_adjacent_rolls(grid, pos) < MAX_ROLLS_ADJACENT
        for pos, char in grid.items()
    )


def solve_part2(data: str) -> int:
    grid = load_grid(data)
    total = 0
    while True:
        to_clear = []
        for pos, char in grid.items():
            if char != ROLL:
                continue
            if get_adjacent_rolls(grid, pos) < MAX_ROLLS_ADJACENT:
                to_clear.append(pos)

        if not to_clear:
            break

        for pos in to_clear:
            grid[pos] = "."
        total += len(to_clear)
    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    part1_result = solve_part1(input_text)
    print(f"Part 1: {part1_result}")
    assert part1_result == 1547

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 8948


if __name__ == "__main__":
    main()
