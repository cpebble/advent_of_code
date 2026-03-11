use std::collections::{HashSet, VecDeque};
use utils;
use utils::{TMaze, Tile};

#[derive(Eq, PartialEq, Debug, Clone, Hash)]
struct Beam {
    r: usize,
    c: usize,
    dir: usize,
}
const PROD: bool = true;
fn main() {
    let inp = utils::load_input(PROD, "day16");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> i32 {
    let layout: TMaze = utils::load_2d_tile_arr(inp);
    let first_beam = Beam {
        r: 0,
        c: 0,
        dir: if PROD { 2 } else { 1 },
    };
    simulate_beam(&layout, vec![first_beam])
}
fn simulate_beam(layout: &TMaze, init_beams: Vec<Beam>) -> i32 {
    let mut seen: HashSet<(isize, isize)> = HashSet::new();
    let mut processed: HashSet<Beam> = HashSet::new();
    let mut beams: VecDeque<Beam> = VecDeque::from(init_beams);
    let ih: isize = layout.height.try_into().unwrap();
    let iw: isize = layout.width.try_into().unwrap();
    while !beams.is_empty() {
        let cur: Beam = beams.pop_front().unwrap();
        if processed.contains(&cur) {
            continue;
        }
        let mut r: isize = cur.r.try_into().unwrap();
        let mut c: isize = cur.c.try_into().unwrap();
        let (dr_, dc_) = utils::COMPASS_DIRECTIONS[cur.dir];
        let dr: isize = dr_.try_into().unwrap();
        let dc: isize = dc_.try_into().unwrap();
        loop {
            seen.insert((r, c));
            // If we are about to take a step outside the grid
            // end loop
            if (r == 0 && dr == -1)
                || (r == ih - 1 && dr == 1)
                || (c == 0 && dc == -1)
                || (c == iw - 1 && dc == 1)
            {
                break;
            }
            r += dr;
            c += dc;
            let tile = layout.maze[r as usize][c as usize];
            // Check if we need to split
            if ((cur.dir == 1 || cur.dir == 3) && tile == Tile::Pipe)
                || ((cur.dir == 0 || cur.dir == 2) && tile == Tile::Dash)
            {
                let b1 = Beam {
                    r: r as usize,
                    c: c as usize,
                    dir: (cur.dir + 1) % 4,
                };
                let b2 = Beam {
                    r: r as usize,
                    c: c as usize,
                    dir: (((cur.dir as isize) - 1).rem_euclid(4)) as usize,
                };
                beams.push_back(b1);
                beams.push_back(b2);
                //println!("Found Split at {r},{c}");
                break;
            }
            if tile == Tile::FSlash {
                beams.push_back(Beam {
                    r: r as usize,
                    c: c as usize,
                    dir: match cur.dir {
                        0 => 1,
                        1 => 0,
                        2 => 3,
                        3 => 2,
                        _ => panic!("Invalid Direction"),
                    },
                });
                break;
            }
            if tile == Tile::BSlash {
                beams.push_back(Beam {
                    r: r as usize,
                    c: c as usize,
                    dir: match cur.dir {
                        0 => 3,
                        1 => 2,
                        2 => 1,
                        3 => 0,
                        _ => panic!("Invalid Direction"),
                    },
                });
                break;
            }
        }
        processed.insert(cur);
    }
    //println!("{}", layout.to_str());
    // let energized = TMaze::generate(layout.height, layout.width, |r, c| {
    // if seen.contains(&(r.try_into().unwrap(), c.try_into().unwrap())) {
    // Tile::Hash
    // } else {
    // Tile::Dot
    // }
    // });
    // println!("{}", energized.to_str());
    return seen.len().try_into().unwrap();
}
fn p2(inp: &str) -> i32 {
    let layout: TMaze = utils::load_2d_tile_arr(inp);
    let mut highest = 0;
    for c in 0..layout.width {
        // Top row
        let ibeams = match layout.maze[0][c] {
            Tile::Dot => vec![Beam { r: 0, c: c, dir: 2 }],
            Tile::FSlash => vec![Beam { r: 0, c: c, dir: 3}],
            Tile::BSlash => vec![Beam { r: 0, c: c, dir: 1}],
            Tile::Pipe => vec![Beam { r: 0, c: c, dir: 2 }],
            Tile::Dash => vec![
                Beam { r: 0, c: c, dir: 3 },
                Beam { r: 0, c: c, dir: 1 }
            ],
            _ => panic!()
        };
        let res = simulate_beam(&layout, ibeams);
        if res > highest { highest = res }
        // Bottom row
        let br = layout.height - 1;
        let ibeams = match layout.maze[br][c] {
            Tile::Dot => vec![Beam { r: br, c: c, dir: 0 }],
            Tile::FSlash => vec![Beam { r: br, c: c, dir: 1}],
            Tile::BSlash => vec![Beam { r: br, c: c, dir: 3}],
            Tile::Pipe => vec![Beam { r: br, c: c, dir: 0 }],
            Tile::Dash => vec![
                Beam { r: br, c: c, dir: 3 },
                Beam { r: br, c: c, dir: 1 }
            ],
            _ => panic!()
        };
        let res = simulate_beam(&layout, ibeams);
        if res > highest { highest = res }

    }
    for r in 0..layout.height {
        // left column
        let ibeams = match layout.maze[r][0] {
            Tile::Dot => vec![Beam { r: r, c: 0, dir: 1 }],
            Tile::FSlash => vec![Beam { r: r, c: 0, dir: 0}],
            Tile::BSlash => vec![Beam { r: r, c: 0, dir: 2}],
            Tile::Dash => vec![Beam { r: r, c: 0, dir: 1 }],
            Tile::Pipe => vec![
                Beam { r: r, c: 0, dir: 0 },
                Beam { r: r, c: 0, dir: 2 }
            ],
            _ => panic!()
        };
        let res = simulate_beam(&layout, ibeams);
        if res > highest { highest = res }

        // right column
        let bc = layout.width - 1;
        let ibeams = match layout.maze[r][bc] {
            Tile::Dot => vec![Beam { r: r, c: bc, dir: 3 }],
            Tile::FSlash => vec![Beam { r: r, c: bc, dir: 2}],
            Tile::BSlash => vec![Beam { r: r, c: bc, dir: 0}],
            Tile::Dash => vec![Beam { r: r, c: bc, dir: 3 }],
            Tile::Pipe => vec![
                Beam { r: r, c: bc, dir: 0 },
                Beam { r: r, c: bc, dir: 2 }
            ],
            _ => panic!()
        };
        let res = simulate_beam(&layout, ibeams);
        if res > highest { highest = res }
    }
    return highest;
}

#[cfg(test)]
mod tests {
    use crate::*;
    #[test]
    pub fn testmod() {
        assert_eq!((-2 as isize).rem_euclid(4), 2);
    }
}
