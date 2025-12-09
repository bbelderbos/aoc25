use std::{env, error::Error, fs, path::PathBuf};

fn solve_part1(input: &str) -> i64 {
    let lines: Vec<&str> = input.lines().collect();

    // Last line = operators, everything above = numbers
    let (ops_line, number_lines) = lines
        .split_last()
        .expect("input must have at least one line");

    // Parse numbers row-wise (whitespace-separated)
    let grid: Vec<Vec<i64>> = number_lines
        .iter()
        .map(|line| {
            line.split_whitespace()
                .map(|tok| tok.parse::<i64>().expect("invalid integer"))
                .collect()
        })
        .collect();

    assert!(!grid.is_empty(), "no numeric rows found");

    let n_rows = grid.len();
    let n_cols = grid[0].len();

    // Transpose rows → columns (each column is one vertical problem)
    let mut cols: Vec<Vec<i64>> = vec![Vec::with_capacity(n_rows); n_cols];
    for (i, row) in grid.iter().enumerate() {
        assert_eq!(
            row.len(),
            n_cols,
            "All rows must have the same number of columns. Expected {}, found {} in row {}",
            n_cols,
            row.len(),
            i
        );
        for (j, &value) in row.iter().enumerate() {
            cols[j].push(value);
        }
    }

    // Ops are whitespace-separated: "*   +   *   +" → ["*", "+", "*", "+"]
    cols.into_iter()
        .zip(ops_line.split_whitespace())
        .map(|(nums, op)| match op {
            "*" => nums.iter().product::<i64>(),
            "+" => nums.iter().sum::<i64>(),
            other => panic!("unexpected operator {other}"),
        })
        .sum()
}

fn solve_part2(input: &str) -> i64 {
    let lines: Vec<&str> = input.lines().collect();
    if lines.is_empty() {
        return 0;
    }

    // Pad all lines to the same width (like Python's ljust)
    let max_width = lines.iter().map(|line| line.len()).max().unwrap();
    let grid: Vec<Vec<char>> = lines
        .iter()
        .map(|line| {
            let mut s = String::with_capacity(max_width);
            s.push_str(line);
            if line.len() < max_width {
                for _ in 0..(max_width - line.len()) {
                    s.push(' ');
                }
            }
            s.chars().collect()
        })
        .collect();

    let n_rows = grid.len();
    let n_cols = max_width;

    let mut total: i64 = 0;
    let mut current: Vec<i64> = Vec::new();

    // Walk columns right-to-left so we collect all numbers in a problem
    // before encountering its operator at the bottom edge.
    for col_idx in (0..n_cols).rev() {
        // Build this column top→bottom
        let col: Vec<char> = grid.iter().map(|row| row[col_idx]).collect();

        // All but the last row are digits (or spaces around them)
        let mut col_num_str: String = col[..n_rows - 1].iter().collect();
        col_num_str = col_num_str.trim().to_string();
        if col_num_str.is_empty() {
            continue; // separator column
        }

        let num: i64 = col_num_str.parse().expect("invalid number in column");
        current.push(num);

        let op = col[n_rows - 1];
        if op == '*' || op == '+' {
            let subtotal = if op == '*' {
                current.iter().product::<i64>()
            } else {
                current.iter().sum::<i64>()
            };
            total += subtotal;
            current.clear();
        }
    }

    // Puzzle guarantees we end exactly on an operator, so current should be empty.
    debug_assert!(current.is_empty());

    total
}

fn read_input(arg: Option<String>) -> Result<String, Box<dyn Error>> {
    let path = match arg {
        Some(p) => PathBuf::from(p),
        None => PathBuf::from("in"), // looks in crate root
    };
    Ok(fs::read_to_string(path)?.trim().to_string())
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input(env::args().nth(1))?;

    let part1 = solve_part1(&input);
    println!("Part 1: {part1}");
    assert_eq!(part1, 4412382293768);

    let part2 = solve_part2(&input);
    println!("Part 2: {part2}");
    assert_eq!(part2, 7858808482092);

    Ok(())
}
