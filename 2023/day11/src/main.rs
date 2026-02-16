use std::collections::HashSet;

use utils::{self, Maze};

fn main() {
    let inp = utils::load_input(true, "day11");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> i32 {
    let image = utils::load_2darr(inp);
    let expanded = expand(image);
    let galaxies: Vec<(usize, usize)> = find_galaxies(expanded).into_iter().collect();
    let mut c = 0;
    for i in 0..galaxies.len() {
        let g1 = galaxies[i];
        for j in i+1..galaxies.len() {
            let g2 = galaxies[j];
            c += utils::manhattan_distance(g1, g2);
        }
    }
    return c.try_into().unwrap();
}

fn find_galaxies(m: Maze) -> HashSet<(usize, usize)> {
    let mut galaxies = HashSet::new();
    for (r, c, e) in &m {
        if e == b'#' {
            galaxies.insert((r, c));
        }
    }
    galaxies
}

fn expand(orig: Maze) -> Maze {
    // Find empty rows and columns
    let mut nonemptyrows: HashSet<usize> = HashSet::new();
    let mut nonemptycols: HashSet<usize> = HashSet::new();

    for r in 0..orig.height {
        for c in 0..orig.width {
            if orig.maze[r][c] == b'#' {
                nonemptycols.insert(c);
                nonemptyrows.insert(r);
            }
        }
    }
    let mut new_rows = Vec::new();
    for r in 0..orig.height {
        let mut new_row = Vec::new();
        for c in 0..orig.width {
            new_row.push(orig.maze[r][c].clone());
            if !nonemptycols.contains(&c) {
                new_row.push(orig.maze[r][c].clone())
            }
        }
        if !nonemptyrows.contains(&r) {
            new_rows.push(new_row.clone());
        }
        new_rows.push(new_row);
    }
    Maze {
        height: orig.height + (orig.height - nonemptyrows.len()),
        width: orig.width + (orig.width - nonemptycols.len()),
        maze: new_rows,
    }
}

fn p2(inp: &str) -> usize {
    let image = utils::load_2darr(inp);
    let allrows: HashSet<usize> = (0..image.height).into_iter().collect();
    let allcols: HashSet<usize> = (0..image.width).into_iter().collect();
    let mut nonemptyrows: HashSet<usize> = HashSet::new();
    let mut nonemptycols: HashSet<usize> = HashSet::new();
    for (r, c, e) in image.into_iter() {
        if e == b'#' {
            nonemptyrows.insert(r);
            nonemptycols.insert(c);
        }
    }
    let emptyrows: HashSet<_> = allrows.difference(&nonemptyrows).collect();
    let emptycols: HashSet<_> = allcols.difference(&nonemptycols).collect();
    let mut galaxies: Vec<(usize, usize)> = Vec::new();
    let mut r_ = 0;
    const EX_FACTOR: usize = 1000000;
    for r in 0..image.height {
        let mut c_ = 0;
        for c in 0..image.width {
            if image.maze[r][c] == b'#' {
                galaxies.push((r_, c_));
            }
            if emptycols.contains(&c) {
                c_ += EX_FACTOR;
            } else {
                c_ += 1;
            }
        }
        if emptyrows.contains(&r) {
            r_ += EX_FACTOR;
        } else {
            r_ += 1;
        }
    }
    let mut c = 0;
    for i in 0..galaxies.len() {
        let g1 = galaxies[i];
        for j in i+1..galaxies.len() {
            let g2 = galaxies[j];
            c += utils::manhattan_distance(g1, g2);
        }
    }
    return c;
}
