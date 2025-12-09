import argparse
from pathlib import Path
from math import dist, prod
from itertools import combinations

NUM_ITERATIONS = 1_000


def solve(data: str, *, part2: bool) -> int:
    n = NUM_ITERATIONS * 1_000 if part2 else NUM_ITERATIONS

    coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]

    # first sort all pairs by distance
    pairs = sorted(
        combinations(coords, 2),
        key=lambda ab: dist(*ab),
    )

    circuits = [{coord} for coord in coords]
    for k, (mina, minb) in enumerate(pairs):
        if k == n:
            break

        ca = cb = set()
        for c in circuits:
            if mina in c:
                ca = c
            if minb in c:
                cb = c

        # already in same circuit, nothing to do
        if ca is cb:
            continue

        new_circuit = ca | cb
        circuits = [c for c in circuits if c not in (ca, cb)]
        circuits.append(new_circuit)

        if part2 and len(circuits) == 1:
            return mina[0] * minb[0]

    sizes = sorted(len(c) for c in circuits)
    return prod(sizes[-3:])


def solve_part1(data: str) -> int:
    return solve(data, part2=False)


def solve_part2(data: str) -> int:
    return solve(data, part2=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    part1_result = solve_part1(input_text)
    print(f"Part 1: {part1_result}")
    assert part1_result == 75680

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 8995844880


if __name__ == "__main__":
    main()
