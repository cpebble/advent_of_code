use std::collections::{HashSet, VecDeque};

use utils;
use utils::TMaze;
use utils::Tile;

#[derive(Debug)]
enum Dir {
    North,
    East,
    South,
    West,
}
impl Dir {
    fn repr(self) -> (isize, isize) {
        match self {
            Dir::North => (-1, 0),
            Dir::East => (0, 1),
            Dir::South => (1, 0),
            Dir::West => (0, -1),
        }
    }
}

#[derive(Debug)]
struct DInst {
    dir: Dir,
    len: usize,
    color: usize,
}

fn main() {
    let inp = utils::load_input(true, "day18");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
// Non-working; initial approach:
// 1. Transform polygon into a Maze
// 2. Flood-fill from edges
// 3. Subtract area from edge to trench
fn trenchmethod(inp: &str) -> usize {
    // First  split up input
    let mut instrs: Vec<DInst> = inp.lines().map(parse_inst).collect();
    // For data shaping, calculate visited coords
    // Then get dimensions
    let (minh, maxh, minw, maxw) = instrs
        .iter()
        .scan((0 as isize, 0 as isize), |(h, w), el| {
            let len: isize = el.len.try_into().unwrap();
            let (h_, w_) = match el.dir {
                Dir::North => (*h - len, *w),
                Dir::South => (*h + len, *w),
                Dir::East => (*h, *w + len),
                Dir::West => (*h, *w - len),
            };
            *h = h_;
            *w = w_;
            Some((h_, w_))
        })
        .fold((0, 0, 0, 0), |(hmi, hma, wmi, wma), (h_, w_)| {
            (
                isize::min(hmi, h_),
                isize::max(hma, h_),
                isize::min(wmi, w_),
                isize::max(wma, w_),
            )
        });
    println!("H: {minh} - {maxh}, W: {minw} - {maxw}");
    let h_calc: usize = (maxh - minh).try_into().unwrap();
    let w_calc: usize = (maxw - minw).try_into().unwrap();
    println!("H: {h_calc}, W: {w_calc}");

    let mut coords: HashSet<(usize, usize)> = HashSet::from([(0, 0)]);
    let mut r = 0 - minh;
    let mut c = 0 - minw;
    for inst in instrs {
        let (dr, dc) = inst.dir.repr();
        for n in 0..inst.len {
            r = r + dr;
            c = c + dc;
            coords.insert((r.try_into().unwrap(), c.try_into().unwrap()));
        }
    }
    let trench: utils::TMaze = TMaze::generate(h_calc + 1, w_calc + 1, |r, c| {
        if coords.contains(&(r, c)) {
            Tile::Hash
        } else {
            Tile::Dot
        }
    });
    //println!("{}", trench.to_str());

    // Now we have a trench; Go through the map and remove any tile connected to the exit
    let init_edges: Vec<(usize, usize)> = trench
        .edges()
        .filter(|(r, c)| trench.maze[*r][*c] == Tile::Dot)
        .collect();
    let mut edgeset: HashSet<(usize, usize)> = HashSet::new();
    let mut to_visit = VecDeque::from(init_edges);

    while to_visit.len() > 0 {
        let (r, c) = to_visit.pop_front().unwrap();
        if edgeset.contains(&(r, c)) {
            continue;
        }
        edgeset.insert((r, c));
        for (tile, r_, c_) in trench.neighbors(r, c) {
            if tile == Tile::Dot {
                to_visit.push_back((r_, c_));
            }
        }
    }
    let filled_trench = TMaze::generate(h_calc + 1, w_calc + 1, |r, c| {
        if edgeset.contains(&(r, c)) {
            Tile::Round
        } else {
            trench.maze[r][c].clone()
        }
    });
    //println!("{}", filled_trench.to_str());
    // Return the area, without edges
    return filled_trench
        .into_iter()
        .map(|(_, _, el)| if el == Tile::Round { 0 } else { 1 })
        .sum();
    // return (trench.height * trench.width) - edgeset.len();
}

fn p1(inp: &str) -> isize {
    let instrs: Vec<DInst> = inp.lines().map(parse_inst).collect();
    let coords: Vec<(isize, isize)> = instrs
        .iter()
        .scan((0 as isize, 0 as isize), |(x, y), el| {
            let len: isize = el.len.try_into().unwrap();
            let (x_, y_) = match el.dir {
                Dir::East => (*x + len, *y),
                Dir::West => (*x - len, *y),
                Dir::North => (*x, *y + len),
                Dir::South => (*x, *y - len),
            };
            *x = x_;
            *y = y_;
            Some((x_, y_))
        })
        .collect();
    let mut arr = 0;
    let N = coords.len();
    for i in 0..N {
        //println!("{i}: {:?} -> {:?}", coords[i], coords[(i+1) % N]);
        arr += utils::determinant_2x2(
            coords[i].0,
            coords[i].1,
            coords[(i + 1) % N].0,
            coords[(i + 1) % N].1,
        );
    }
    let arr = isize::abs(arr);
    // Try to reorder pick's theorem
    let boundary_points: isize = instrs
        .iter()
        .fold(0, |acc, el| acc + (*el).len)
        .try_into()
        .unwrap();
    //println!("{boundary_points}");

    // A = i + b/2 - 1
    // A - (b/2) = i - 1
    let interior = (arr / 2) - (boundary_points / 2) + 1;
    //println!("{interior}");
    return interior + boundary_points;
    //return arr / 2;
}

fn p2(inp: &str) -> isize {
    let instrs: Vec<DInst> = inp.lines().map(parse_inst_2).collect();
    let coords: Vec<(isize, isize)> = instrs
        .iter()
        .scan((0 as isize, 0 as isize), |(x, y), el| {
            let len: isize = el.len.try_into().unwrap();
            let (x_, y_) = match el.dir {
                Dir::East => (*x + len, *y),
                Dir::West => (*x - len, *y),
                Dir::North => (*x, *y + len),
                Dir::South => (*x, *y - len),
            };
            *x = x_;
            *y = y_;
            Some((x_, y_))
        })
        .collect();
    let mut arr = 0;
    let N = coords.len();
    for i in 0..N {
        //println!("{i}: {:?} -> {:?}", coords[i], coords[(i+1) % N]);
        arr += utils::determinant_2x2(
            coords[i].0,
            coords[i].1,
            coords[(i + 1) % N].0,
            coords[(i + 1) % N].1,
        );
    }
    let arr = isize::abs(arr);
    // Try to reorder pick's theorem
    let boundary_points: isize = instrs
        .iter()
        .fold(0, |acc, el| acc + (*el).len)
        .try_into()
        .unwrap();

    // A = i + b/2 - 1
    // A - (b/2) = i - 1
    let interior = (arr / 2) - (boundary_points / 2) + 1;

    return interior + boundary_points;
}

fn parse_inst(inp: &str) -> DInst {
    let lsplit: Vec<&str> = inp.split(' ').collect();
    DInst {
        dir: match lsplit[0] {
            "R" => Dir::East,
            "L" => Dir::West,
            "U" => Dir::North,
            "D" => Dir::South,
            s => panic!("Direction not recognized: {s}"),
        },
        len: lsplit[1].parse::<usize>().unwrap(),
        color: parse_col(lsplit[2]),
    }
}
fn parse_inst_2(inp: &str) -> DInst {
    let lsplit: Vec<&str> = inp.split(' ').collect();

    let trimmed = lsplit[2].trim_start_matches("(#").trim_end_matches(")");
    DInst {
        dir: match trimmed.chars().nth(5).unwrap() {
            '0' => Dir::East,
            '1' => Dir::South,
            '2' => Dir::West,
            '3' => Dir::North,
            s => panic!("Direction not recognized:{} {s}", lsplit[2]),
        },
        len: usize::from_str_radix(&trimmed[0..5], 16).unwrap(),
        color: parse_col(lsplit[2]),
    }
}

fn parse_col(inp: &str) -> usize {
    let trimmed = inp.trim_start_matches("(#").trim_end_matches(")");
    let parsed = usize::from_str_radix(trimmed, 16).unwrap();
    return parsed;
}
