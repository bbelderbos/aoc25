# /// script
# dependencies = [
#   "polyomino"
# ]
# ///
import argparse
from functools import cache
from pathlib import Path

from polyomino.board import Rectangle
from polyomino.error import CantPlaceSinglePiece
from polyomino.tileset import CoverWithWrongModulus, CoverWithWrongSize, any_number_of

Cell = tuple[int, int]
Counts = tuple[int, int, int, int, int, int]


def parse_shapes(text: str) -> list[frozenset[Cell]]:
    blocks = text.split("\n\n")[:-1]
    grids = []
    for block in blocks:
        grid = [line.strip() for line in block.splitlines()[1:]]
        grids.append(
            frozenset(
                (x, y)
                for y, row in enumerate(grid)
                for x, ch in enumerate(row)
                if ch == "#"
            )
        )
    return grids


def parse_region_lines(text: str) -> list[tuple[int, int, list[int]]]:
    blocks = text.split("\n\n")

    def _parse_line(line: str) -> tuple[int, int, list[int]]:
        left, right = line.split(":", 1)
        w, h = map(int, left.split("x", 1))
        counts = [int(x) for x in right.split()]
        return (w, h, counts)

    return [_parse_line(line) for line in blocks[-1].splitlines()]


def solve(data: str) -> int:
    shapes = parse_shapes(data)
    regions = parse_region_lines(data)

    tiles = tuple(tuple(sorted(s)) for s in shapes)  # stable / hashable
    mono = [(0, 0)]  # filler for leftover cells

    @cache
    def can_pack(w: int, h: int, counts: Counts) -> bool:
        board = Rectangle(w, h)

        # start with "free filler" so we don't require full cover by the given pieces
        tileset = any_number_of([mono])

        # add the mandatory multiset of pieces (exactly the counts)
        for t, c in zip(tiles, counts):
            if c:
                tileset = tileset.and_repeated_exactly(c, list(t))

        try:
            return board.tile_with_set(tileset).solve() is not None
        except (CoverWithWrongSize, CoverWithWrongModulus, CantPlaceSinglePiece):
            return False

    return sum(can_pack(w, h, tuple(counts_list)) for w, h, counts_list in regions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default=Path(__file__).with_name("in"))
    args = parser.parse_args()

    input_text = Path(args.path).read_text().strip()

    result = solve(input_text)
    print(f"Part 1: {result}")
    assert result == 479


if __name__ == "__main__":
    main()
