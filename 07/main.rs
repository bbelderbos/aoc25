use std::collections::HashMap;
use std::{env, error::Error, fs, path::PathBuf};

fn load_grid(data: &str) -> Vec<Vec<char>> {
    data.lines().map(|line| line.chars().collect()).collect()
}

fn find_char_in_row(row: &[char], target: char) -> Option<usize> {
    row.iter().position(|&c| c == target)
}

fn solve(input: &str, part2: bool) -> i64 {
    let grid = load_grid(input);
    let start_col = find_char_in_row(&grid[0], 'S').expect("Start 'S' not found in the first row");

    let mut beams: HashMap<usize, i64> = HashMap::from([(start_col, 1)]);
    let mut total_splits = 0;

    for row in grid.iter().skip(1) {
        let mut new_beams = HashMap::new();
        for (&pos, &count) in beams.iter() {
            if row[pos] == '^' {
                debug_assert!(pos > 0 && pos + 1 < row.len());
                total_splits += 1;
                for new_pos in [pos - 1, pos + 1] {
                    *new_beams.entry(new_pos).or_insert(0) += count;
                }
            } else {
                *new_beams.entry(pos).or_insert(0) += count;
            }
        }
        beams = new_beams;
    }
    if part2 {
        beams.values().sum()
    } else {
        total_splits
    }
}

fn solve_part1(input: &str) -> i64 {
    solve(input, false)
}
fn solve_part2(input: &str) -> i64 {
    solve(input, true)
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
    assert_eq!(part1, 1651);

    let part2 = solve_part2(&input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 108924003331749);

    Ok(())
}
