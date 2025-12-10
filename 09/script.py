import argparse
from pathlib import Path
from itertools import combinations, pairwise
from dataclasses import dataclass


@dataclass(frozen=True)
class Segment:
    vertical: bool
    fixed: int  # x if vertical, y if horizontal
    start: int  # inclusive
    end: int  # inclusive


def inclusive_area(a, b):
    x1, y1 = a
    x2, y2 = b
    return (abs(x2 - x1) + 1) * (abs(y2 - y1) + 1)


def solve_part1(data: str) -> int:
    coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]
    return max(inclusive_area(a, b) for a, b in combinations(coords, 2))


def segment_between(a: tuple[int, int], b: tuple[int, int]) -> Segment:
    x1, y1 = a
    x2, y2 = b
    if x1 == x2:  # vertical
        lo, hi = sorted((y1, y2))
        return Segment(vertical=True, fixed=x1, start=lo, end=hi)
    elif y1 == y2:  # horizontal
        lo, hi = sorted((x1, x2))
        return Segment(vertical=False, fixed=y1, start=lo, end=hi)
    else:
        raise ValueError("Input guarantees axis-aligned adjacency only")


def point_in_polygon(px: float, py: float, edges: list[tuple[int, int]]) -> bool:
    inside = False
    for (x1, y1), (x2, y2) in edges:
        # Ignore horizontal edges for crossing logic
        if y1 == y2:
            continue
        # Does the edge straddle py?
        if (y1 > py) != (y2 > py):
            # x coordinate where this edge crosses scanline at y=py
            x_cross = x1 + (py - y1) * (x2 - x1) / (y2 - y1)
            if x_cross > px:
                inside = not inside
    return inside


def polygon_crosses_rect_interior(
    x1: int, y1: int, x2: int, y2: int, segments: list[Segment]
) -> bool:
    for s in segments:
        if s.vertical:
            x = s.fixed
            if x1 < x < x2:
                # overlap of (y1, y2) with [start, end]
                if max(s.start, y1) < min(s.end, y2):
                    return True
        else:
            y = s.fixed
            if y1 < y < y2:
                # overlap of (x1, x2) with [start, end]
                if max(s.start, x1) < min(s.end, x2):
                    return True
    return False


def solve_part2(data: str) -> int:
    coords = [tuple(map(int, line.split(","))) for line in data.splitlines()]
    edges = list(pairwise(coords + [coords[0]]))
    segments: list[Segment] = [segment_between(a, b) for a, b in edges]
    max_area = 0

    for a, b in combinations(coords, 2):
        x1, y1 = a
        x2, y2 = b

        # skip non-rectangles (need different x AND y)
        if x1 == x2 or y1 == y2:
            continue

        # normalize
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        dx = x2 - x1
        dy = y2 - y1
        area = (dx + 1) * (dy + 1)

        if area <= max_area:
            continue

        # 1) center must be inside polygon
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0
        if not point_in_polygon(cx, cy, edges):
            continue

        # 2) polygon must not cross interior of rectangle
        if polygon_crosses_rect_interior(x1, y1, x2, y2, segments):
            continue

        max_area = area

    return max_area


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    part1_result = solve_part1(input_text)
    print(f"Part 1: {part1_result}")
    assert part1_result == 4746238001

    part2_result = solve_part2(input_text)
    print(f"Part 2: {part2_result}")
    assert part2_result == 1552139370


if __name__ == "__main__":
    main()
