import argparse
from pathlib import Path


def parse_ranges(block: str) -> list[tuple[int, int]]:
    return [tuple(map(int, line.split("-"))) for line in block.splitlines()]


def ingredient_in_range(ingredient: int, ranges: list[tuple[int, int]]) -> bool:
    return any(start <= ingredient <= end for start, end in ranges)


def solve_part1(data: str) -> int:
    range_block, ingredient_block = data.split("\n\n")
    ranges = parse_ranges(range_block)
    ingredients = [int(x) for x in ingredient_block.splitlines()]
    return sum(ingredient_in_range(in_, ranges) for in_ in ingredients)


def solve_part2(data: str) -> int:
    ranges_block = data.split("\n\n")[0]
    ranges = sorted(parse_ranges(ranges_block))

    covered_end = -1
    total = 0

    for start, end in ranges:
        if end <= covered_end:
            # fully covered, skip
            continue
        if start <= covered_end:
            # trim the subrange already covered
            start = covered_end + 1

        total += end + 1 - start
        covered_end = end

    return total


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    part1_result = solve_part1(input_text)
    print(f"Part 1: {part1_result}")
    assert part1_result == 623

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 353507173555373


if __name__ == "__main__":
    main()
