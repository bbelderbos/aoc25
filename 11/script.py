import argparse
from collections import defaultdict
from functools import cache
from pathlib import Path


def parse_graph(data: str) -> dict[str, list[str]]:
    graph = defaultdict(list)
    for line in data.splitlines():
        parent, children_str = line.split(": ")
        graph[parent].extend(children_str.split())
    return graph


def solve(data: str, part2: bool = False) -> int:
    graph = parse_graph(data)
    start = "svr" if part2 else "you"
    target = "out"

    must_visit = {"dac", "fft"} if part2 else set()

    @cache
    def count(node: str, visited: frozenset[str]) -> int:
        if node in must_visit:
            visited = visited | {node}

        if node == target:
            # only count paths where we've seen all required nodes
            return int(must_visit.issubset(visited))

        return sum(count(child, visited) for child in graph[node])

    return count(start, frozenset())


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
    assert part1_result == 724

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 473930047491888


if __name__ == "__main__":
    main()
