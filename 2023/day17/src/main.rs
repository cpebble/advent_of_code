use std::collections::{BinaryHeap, HashMap, HashSet};

use utils;
use utils::IMaze;

type UMaze = IMaze<usize>;

#[derive(PartialEq, Eq, Debug)]
struct QObj {
    cords: (usize, usize),
    dist: usize,
    consec: usize,
    dir: usize,
}
impl Ord for QObj {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.dist.cmp(&self.dist)
    }
}

impl PartialOrd for QObj {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}
//impl PartialOrd for QObj {
//fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
//match self.cords.partial_cmp(&other.cords) {
//Some(core::cmp::Ordering::Equal) => {}
//ord => return ord,
//}
//self.dist.partial_cmp(&other.dist)
//}
//}

fn main() {
    let inp = utils::load_input(false, "day17");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> usize {
    let _map = utils::load_2darr(inp);
    let map = UMaze::generate(_map.height, _map.width, |r, c| {
        ((_map.maze[r][c]) - 0x30).into()
    });
    //println!("{}", map.to_str());
    djks(&map)

}
fn djks(map: &UMaze) -> usize {
    let mut heap: BinaryHeap<QObj> = BinaryHeap::new();
    let mut dist: HashMap<(usize, usize), usize> = HashMap::new();
    heap.push(QObj {
        cords: (0, 0),
        dist: 0,
        consec: 0,
        dir: 1,
    });
    let mut i = 0;
    while i < 1000000 && heap.peek().is_some() {
        i += 1;
        // Fetch Shortest Qo
        let qo = heap.pop().unwrap();
        println!("QO: {:?}\nSeen: {}", qo, dist.len());
        let (r, c) = qo.cords;
        let di = qo.dir;
        
        // Check if is end
        if r == map.height - 1 && c == map.width - 1 {
            return qo.dist;
        }
        // Else calc possible places to go
        let mut possible = vec![((di + 3) % 4, 0), ((di + 1) % 4, 0)];
        if qo.consec < 2 {
            possible.push((di, qo.consec + 1));
        }
        // For each possible neighbor
        for (di_, cnew) in possible {
            // Get directions
            let (dr, dc) = utils::COMPASS_DIRECTIONS[di_];
            // Filter out off-neighbor maps
            if (r == 0 && dr < 0)
                || (r == map.height - 1 && dr > 0)
                || (c == 0 && dc < 0)
                || (c == map.width - 1 && dc > 0)
            {
                continue;
            }
            let c_ = ((c as isize) + (dc as isize)) as usize;
            let r_ = ((r as isize) + (dr as isize)) as usize;
            //println!("{}, {}, {}", r, dr, r_);
            let cur_dist = qo.dist + map.maze[r][c]; 
            let rec_dist = dist.get(&(r_, c_)).unwrap_or(&usize::MAX);
            if *rec_dist <= cur_dist  {
                continue;
            }
            dist.insert((r_, c_), cur_dist);
            heap.push(QObj {
                cords: (r_, c_),
                dist: cur_dist, 
                consec: cnew,
                dir: di_,
            });

        }
    }
    return 0;
}
fn djks__(map: &UMaze) -> usize {
    let mut heap: BinaryHeap<QObj> = BinaryHeap::new();
    let mut dist: HashMap<(usize, usize), usize> = HashMap::new();
    let mut prev: HashMap<(usize, usize), (usize, usize)> = HashMap::new();
    heap.push(QObj {
        cords: (0, 0),
        dist: 0,
        consec: 0,
        dir: 1,
    });
    let mut i = 0;
    while i < 1000000 && heap.peek().is_some() {
        i += 1;
        let qo = heap.pop().unwrap();
        println!("QO: {:?}\nSeen: {}", qo, dist.len());
        let (r, c) = qo.cords;
        let di = qo.dir;
        let mut possible = vec![((di + 3) % 4, 0), ((di + 1) % 4, 0)];
        if qo.consec < 1 {
            possible.push((di, qo.consec + 1));
        }
        for (di_, cnew) in possible {
            let (dr, dc) = utils::COMPASS_DIRECTIONS[di_];
            if (r == 0 && dr < 0)
                || (r == map.height - 1 && dr > 0)
                || (c == 0 && dc < 0)
                || (c == map.width - 1 && dc > 0)
            {
                continue;
            }
            let c_ = ((c as isize) + (dc as isize)) as usize;
            let r_ = ((r as isize) + (dr as isize)) as usize;
            println!("{}, {}, {}", r, dr, r_);

            match dist.get(&(r_, c_)) {
                Some(d) => {
                    if *d < (qo.dist + map.maze[r][c]) {
                        continue;
                    }
                }
                None => (),
            };
            dist.insert((r_, c_), qo.dist + map.maze[r][c]);
            prev.insert((r_, c_), qo.cords.clone());
            heap.push(QObj {
                cords: (r_, c_),
                dist: qo.dist + map.maze[r][c],
                consec: cnew,
                dir: di_,
            });

            let mut cur = Some(&(r_, c_));
            let mut path: Vec<&(usize, usize)> = Vec::new();
            while cur.is_some() {
                path.push(cur.unwrap());
                cur = prev.get(&(cur.unwrap()));
            }
            println!("{:?}", path);
            println!(
                "{}",
                IMaze::generate(map.height, map.width, |r, c| {
                    if path.contains(&&(r, c)) {
                        '#' as u8
                    } else {
                        '.' as u8
                    }
                })
                .to_str()
            );
        }
    }
    let mut cur = Some(&(map.height - 1, map.width - 1));
    let mut path: Vec<&(usize, usize)> = Vec::new();
    while cur.is_some() {
        path.push(cur.unwrap());
        cur = prev.get(&(cur.unwrap()));
    }
    println!("{:?}", path);
    println!(
        "{}",
        IMaze::generate(map.height, map.width, |r, c| {
            if path.contains(&&(r, c)) {
                '#' as u8
            } else {
                '.' as u8
            }
        })
        .to_str()
    );
    println!("{:?}", dist.get(&(map.height - 1, map.width - 1)));
    return 0;
}
fn p2(inp: &str) -> i32 {
    return 0;
}
