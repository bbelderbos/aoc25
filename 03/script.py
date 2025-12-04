import argparse
from pathlib import Path


def find_largest_k_digit_number(row: str, k: int) -> str:
    if k > len(row):
        raise ValueError(f"k={k} is greater than the length of row ({len(row)}): {row!r}")
    num_drops = len(row) - k
    stack = []

    for ch in row:
        while num_drops and stack and stack[-1] < ch:
            stack.pop()
            num_drops -= 1
        stack.append(ch)

    return "".join(stack[:k])


def solve(data: str, part2: bool = False) -> int:
    numbers = []
    for row in data.splitlines():
        best = find_largest_k_digit_number(row, 12 if part2 else 2)
        numbers.append(best)
    return sum(int(num) for num in numbers)


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
    assert part1_result == 17330

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 171518260283767


if __name__ == "__main__":
    main()

