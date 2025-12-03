use std::{env, error::Error, fs, path::PathBuf};

fn find_largest_k_digit_number(row: &str, k: usize) -> i64 {
    let mut num_drops = row.len() - k;
    let mut stack: Vec<char> = Vec::new();
    for ch in row.chars() {
        while num_drops > 0 {
            if let Some(&last) = stack.last() {
                if last < ch {
                    stack.pop();
                    num_drops -= 1;
                    continue;
                }
            }
            break;
        }
        stack.push(ch);
    }
    stack
        .iter()
        .take(k)
        .collect::<String>()
        .parse::<i64>()
        .expect("Failed to parse to i64")
}

fn solve(data: &str, part2: bool) -> i64 {
    data.lines()
        .map(|line| find_largest_k_digit_number(line, if part2 { 12 } else { 2 }))
        .sum()
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
    assert_eq!(part1, 17330);

    let part2 = solve_part2(&input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 171518260283767);

    Ok(())
}

