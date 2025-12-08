use std::collections::{HashMap, HashSet};
use std::{env, error::Error, fs, path::PathBuf};

const NUM_ITERATIONS: usize = 1_000;

fn dist2(a: (i64, i64, i64), b: (i64, i64, i64)) -> i64 {
    let dx = a.0 - b.0;
    let dy = a.1 - b.1;
    let dz = a.2 - b.2;
    dx * dx + dy * dy + dz * dz
}

fn solve(data: &str, part2: bool) -> i64 {
    let n = NUM_ITERATIONS * if part2 { 1_000 } else { 1 };

    let coords: Vec<(i64, i64, i64)> = data
        .lines()
        .map(|line| {
            let mut parts = line.split(',');
            let x = parts.next().unwrap().parse::<i64>().unwrap();
            let y = parts.next().unwrap().parse::<i64>().unwrap();
            let z = parts.next().unwrap().parse::<i64>().unwrap();
            (x, y, z)
        })
        .collect();

    let m = coords.len();

    // all pairs: (dist², index_a, index_b)
    let mut pairs: Vec<(i64, usize, usize)> = Vec::new();
    for i in 0..m {
        for j in (i + 1)..m {
            let d2 = dist2(coords[i], coords[j]);
            pairs.push((d2, i, j));
        }
    }
    pairs.sort_unstable_by_key(|&(d2, _, _)| d2);
    let limit = n.min(pairs.len());

    // circuits as sets of coords, like Python
    let mut circuits: Vec<HashSet<(i64, i64, i64)>> = coords
        .iter()
        .map(|&c| {
            let mut hs = HashSet::new();
            hs.insert(c);
            hs
        })
        .collect();

    // coord -> circuit index, for O(1) lookup
    let mut owner: HashMap<(i64, i64, i64), usize> = HashMap::new();
    for (idx, c) in coords.iter().enumerate() {
        owner.insert(*c, idx);
    }

    // track number of non-empty circuits (instead of shrinking the Vec)
    let mut active_circuits = m;

    for &(_, ai, bi) in pairs.iter().take(limit) {
        let mina = coords[ai];
        let minb = coords[bi];

        let ca_idx = match owner.get(&mina) {
            Some(&idx) => idx,
            None => continue,
        };
        let cb_idx = match owner.get(&minb) {
            Some(&idx) => idx,
            None => continue,
        };

        // already in same circuit, nothing to do
        if ca_idx == cb_idx {
            continue;
        }

        // merge smaller into larger for fewer moves
        let (keep_idx, drop_idx) = if circuits[ca_idx].len() >= circuits[cb_idx].len() {
            (ca_idx, cb_idx)
        } else {
            (cb_idx, ca_idx)
        };

        // move all coords from drop -> keep and update owner
        let moved: Vec<(i64, i64, i64)> = circuits[drop_idx].drain().collect();
        for p in moved {
            circuits[keep_idx].insert(p);
            owner.insert(p, keep_idx);
        }
        active_circuits -= 1;

        if part2 && active_circuits == 1 {
            return coords[ai].0 * coords[bi].0;
        }
    }

    // part 1: sizes of all non-empty circuits
    let mut sizes: Vec<usize> = circuits
        .iter()
        .filter(|c| !c.is_empty())
        .map(|c| c.len())
        .collect();

    sizes.sort_unstable();
    let len = sizes.len();
    (sizes[len - 1] * sizes[len - 2] * sizes[len - 3]) as i64
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
        None => PathBuf::from("in"),
    };
    Ok(fs::read_to_string(path)?.trim().to_string())
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = read_input(env::args().nth(1))?;
    let part1 = solve_part1(&input);
    println!("Part 1: {part1}");
    assert_eq!(part1, 75680);

    let part2 = solve_part2(&input);
    println!("Part 2: {part2}");
    assert_eq!(part2, 8995844880);

    Ok(())
}
