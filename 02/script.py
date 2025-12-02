import argparse
from pathlib import Path


def has_repeated_halves(s: str) -> bool:
    n = len(s)
    if n % 2:
        return False

    mid = n // 2
    first, last = s[:mid], s[mid:]

    if first[0] == "0" or last[0] == "0":
        return False

    return first == last


def has_repeated_chunks(s: str) -> bool:
    n = len(s)
    for size in range(1, n // 2 + 1):
        if n % size != 0:
            continue

        chunk = s[:size]
        if chunk * (n // size) == s:
            return True

    return False


def solve(data: str, part2: bool = False) -> int:
    total = 0
    for row in data.split(","):
        start, end = map(int, row.split("-"))
        for i in range(start, end + 1):
            s = str(i)
            if has_repeated_halves(s):
                total += i
            elif part2 and has_repeated_chunks(s):
                total += i
    return total


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
    assert part1_result == 31839939622

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 41662374059


if __name__ == "__main__":
    main()
