use std::{env, error::Error, fs, path::PathBuf};

fn parse_ranges(block: &str) -> Vec<(i64, i64)> {
    let mut ranges: Vec<(i64, i64)> = block
        .lines()
        .map(|line| {
            let (start, end) = line.split_once('-').unwrap();
            let start: i64 = start.parse().unwrap();
            let end: i64 = end.parse().unwrap();
            (start, end)
        })
        .collect();

    ranges.sort_unstable_by_key(|(start, _)| *start);
    ranges
}

fn ingredient_in_range(ingredient: i64, ranges: &[(i64, i64)]) -> bool {
    ranges
        .iter()
        .take_while(|(start, _)| ingredient >= *start)
        .any(|(start, end)| ingredient >= *start && ingredient <= *end)
}

fn solve_part1(input: &str) -> i64 {
    let mut parts = input.split("\n\n");
    let range_block = parts.next().unwrap();
    let ingredient_block = parts.next().unwrap();

    let ranges = parse_ranges(range_block);

    ingredient_block
        .lines()
        .map(|line| line.parse::<i64>().unwrap())
        .filter(|&ingredient| ingredient_in_range(ingredient, &ranges))
        .count() as i64
}

fn solve_part2(input: &str) -> i64 {
    let mut parts = input.split("\n\n");
    let range_block = parts.next().unwrap();
    let ranges = parse_ranges(range_block);

    let mut covered_end = -1;
    let mut total = 0;

    for (start, end) in ranges {
        if end <= covered_end {
            continue;
        }
        let new_start = start.max(covered_end + 1);
        total += end + 1 - new_start;
        covered_end = end;
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
    assert_eq!(part1, 623);

    let part2 = solve_part2(&input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 353507173555373);

    Ok(())
}
