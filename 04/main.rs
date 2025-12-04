use std::collections::HashMap;
use std::{env, error::Error, fs, path::PathBuf};

const ROLL: char = '@';
const MAX_ROLLS_ADJACENT: usize = 4;

#[derive(Clone, Copy, Eq, PartialEq, Hash)]
struct Position {
    x: i32,
    y: i32,
}

const DIRECTIONS: [Position; 8] = [
    Position { x: -1, y: -1 },
    Position { x: 0, y: -1 },
    Position { x: 1, y: -1 },
    Position { x: -1, y: 0 },
    Position { x: 1, y: 0 },
    Position { x: -1, y: 1 },
    Position { x: 0, y: 1 },
    Position { x: 1, y: 1 },
];

fn load_grid(data: &str) -> HashMap<Position, char> {
    let mut grid = HashMap::new();
    for (y, line) in data.lines().enumerate() {
        for (x, ch) in line.chars().enumerate() {
            grid.insert(
                Position {
                    x: x as i32,
                    y: y as i32,
                },
                ch,
            );
        }
    }
    grid
}

fn get_adjacent_rolls(grid: &HashMap<Position, char>, pos: Position) -> usize {
    DIRECTIONS
        .iter()
        .filter(|d| {
            let adj = Position {
                x: pos.x + d.x,
                y: pos.y + d.y,
            };
            grid.get(&adj) == Some(&ROLL)
        })
        .count()
}

fn solve_part1(input: &str) -> i64 {
    let grid = load_grid(input);

    grid.iter()
        .filter(|(&pos, &ch)| ch == ROLL && get_adjacent_rolls(&grid, pos) < MAX_ROLLS_ADJACENT)
        .count() as i64
}

fn solve_part2(input: &str) -> i64 {
    let mut grid = load_grid(input);
    let mut total = 0;

    loop {
        let mut to_clear = Vec::new();

        // First pass: read-only scan to decide which positions to clear.
        // In Rust we can't mutate `grid` while iterating `grid.iter()`,
        // so we collect positions to change and apply the mutations afterwards.
        for (&pos, &ch) in grid.iter() {
            if ch != ROLL {
                continue;
            }
            if get_adjacent_rolls(&grid, pos) < MAX_ROLLS_ADJACENT {
                to_clear.push(pos);
            }
        }

        if to_clear.is_empty() {
            break;
        }

        // Second pass: apply mutations now that no immutable borrows are active.
        total += to_clear.len() as i64;
        for pos in to_clear {
            grid.insert(pos, '.');
        }
    }

    total
}

fn read_input(arg: Option<String>) -> Result<String, Box<dyn Error>> {
    let path = match arg {
        Some(p) => PathBuf::from(p),
        None => std::path::PathBuf::from("in"), // looks in crate root
    };
    Ok(fs::read_to_string(path)?.trim().to_string())
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input(env::args().nth(1))?;
    let part1 = solve_part1(&input);
    println!("Part 1: {}", part1);
    assert_eq!(part1, 1547);

    let part2 = solve_part2(&input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 8948);

    Ok(())
}
