use std::cmp::min;

use utils;
use utils::{IMaze, Tile};

type TMaze = IMaze<Tile>;

fn main() {
    let inp = utils::load_input(true, "day13");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> i32 {
    let ms: Vec<TMaze> = inp
        .split("\n\n")
        .map(utils::load_2darr)
        .map(|m| m.into())
        .collect();

    let mut i = 0;
    let mut total = 0;
    for m in ms {
        i += 1;
        let symm = |m: &IMaze<Tile>| {
            for r in 0..m.height - 1 {
                if is_mirror_h(m, r, true) {
                    return (r + 1) * 100;
                }
            }
            for c in 0..m.width - 1 {
                if is_mirror_v(m, c, true) {
                    return c + 1;
                }
            }
            panic!("Couldn't find solution for maze {}:\n{}", i, m.to_str());
            return 0;
        };
        total += symm(&m);
    }
    return total.try_into().unwrap();
}

// 2
//
// for d in 0..(2, 7-3=4)
// (0), 2, 3
// (1), 1, 4
// (2), 0, 5
fn is_mirror_h(m: &TMaze, row: usize, smudge: bool) -> bool {
    let mut _smudge = smudge;
    for d in 0..row + 1 {
        if row + 1 + d >= m.height {
            continue;
        }
        for c in 0..m.width {
            if m.maze[row + 1 + d][c] != m.maze[row - d][c] {
                if !_smudge {
                    _smudge = true;
                } else {
                    return false;
                }
            }
        }
    }
    return _smudge;
}
//fn is_mirror_h(m: &TMaze, row: usize) -> bool {
//// Approach row from one side
//let irow: isize = row.into();
//let offset_r = irow - current_r;
//for r in 0..row {
//// Invariant: r < r_mid
//if row + 1 + r
//}
//}

fn is_mirror_v(m: &TMaze, col: usize, smudge: bool) -> bool {
    let mut _smudge = smudge;
    for d in 0..col + 1 {
        if col + 1 + d >= m.width {
            continue;
        }
        for r in 0..m.height {
            if m.maze[r][col + 1 + d] != m.maze[r][col - d] {
                if !_smudge {
                    _smudge = true;
                } else {
                    return false;
                }
            }
        }
    }
    return _smudge;
}
fn p2(inp: &str) -> i32 {
    let ms: Vec<TMaze> = inp
        .split("\n\n")
        .map(utils::load_2darr)
        .map(|m| m.into())
        .collect();

    let mut i = 0;
    let mut total = 0;
    for m in ms {
        i += 1;
        let symm = |m: &IMaze<Tile>| {
            for r in 0..m.height - 1 {
                if is_mirror_h(m, r, false) {
                    return (r + 1) * 100;
                }
            }
            for c in 0..m.width - 1 {
                if is_mirror_v(m, c, false) {
                    return c + 1;
                }
            }
            panic!("Couldn't find solution for maze {}:\n{}", i, m.to_str());
            return 0;
        };
        total += symm(&m);
    }
    return total.try_into().unwrap();
}
