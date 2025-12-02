use std::{env, error::Error, fs, path::PathBuf};

fn has_repeated_halves(s: &str) -> bool {
    let n = s.len();
    if n % 2 != 0 {
        return false;
    }

    let mid = n / 2;
    let (first_half, second_half) = s.split_at(mid);

    // if either starts with 0 return false
    if first_half.starts_with('0') || second_half.starts_with('0') {
        return false;
    }

    first_half == second_half
}

fn has_repeated_chunks(s: &str) -> bool {
    let n = s.len();
    let bytes = s.as_bytes();

    for size in 1..=n / 2 {
        if n % size != 0 {
            continue;
        }
        let first = &bytes[..size];
        if bytes.chunks(size).all(|c| c == first) {
            return true;
        }
    }
    false
}

fn solve(input: &str, part2: bool) -> i64 {
    let mut total = 0;
    for line in input.split(",") {
        let (start, end) = {
            let (s, e) = line.trim().split_once('-').expect("start-end");
            (
                s.parse::<i64>().expect("start"),
                e.parse::<i64>().expect("end"),
            )
        };
        for x in start..=end {
            let id = x.to_string();

            if has_repeated_halves(&id) || (part2 && has_repeated_chunks(&id)) {
                total += x;
            }
        }
    }
    total
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
    assert_eq!(part1, 31839939622);

    let part2 = solve_part2(&input);
    println!("Part 2: {}", part2);
    assert_eq!(part2, 41662374059);

    Ok(())
}
