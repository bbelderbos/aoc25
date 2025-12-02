use std::{env, error::Error, fs, path::PathBuf};

const DIAL_SIZE: i32 = 100;
const START: i32 = 50;

fn step(pos: i32, rot: char, amount: i32) -> i32 {
    match rot {
        'L' => (pos - amount + DIAL_SIZE) % DIAL_SIZE,
        'R' => (pos + amount) % DIAL_SIZE,
        _ => panic!("Invalid direction"),
    }
}

fn parse_line(line: &str) -> (char, i32) {
    let (dir, amount) = line.split_at(1);
    let dir = dir.chars().next().expect("direction char at start of line");
    let amount = amount
        .parse::<i32>()
        .expect("numeric amount after direction");
    (dir, amount)
}

fn solve_part1(input: &str) -> i64 {
    let mut pos = START;
    let mut pw = 0;
    for line in input.lines() {
        let (dir, amount) = parse_line(line);
        pos = step(pos, dir, amount);
        if pos == 0 {
            pw += 1
        }
    }
    pw
}

fn solve_part2(input: &str) -> i64 {
    let mut pos = START;
    let mut pw = 0;
    for line in input.lines() {
        let (dir, amount) = parse_line(line);
        for _ in 0..amount {
            pos = step(pos, dir, 1);
            if pos == 0 {
                pw += 1
            }
        }
    }
    pw
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
    assert_eq!(part1, 1055);

    let part2 = solve_part2(&input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 6386);

    Ok(())
}
