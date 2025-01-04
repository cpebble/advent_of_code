use utils::{self, neighbors_2d, Maze};

fn main() {
    let inp = utils::load_input(true, "day3");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}

const SYMBOLS: [char; 10] = ['#', '$', '%', '&', '*', '+', '-', '/', '=', '@'];
fn issymbol(c: &u8) -> bool {
    return c == &('#' as u8)
        || c == &('$' as u8)
        || c == &('%' as u8)
        || c == &('&' as u8)
        || c == &('*' as u8)
        || c == &('+' as u8)
        || c == &('-' as u8)
        || c == &('/' as u8)
        || c == &('=' as u8)
        || c == &('@' as u8);
}
fn p1(inp: &str) -> i32 {
    let maze_s = utils::load_2darr(inp);
    let Maze {
        height,
        width,
        ref maze,
    } = maze_s;
    let mut sum = 0;
    for r in 0..height {
        let mut c = 0;
        while c < width {
            let cha = maze[r][c];
            if cha.is_ascii_digit() {
                let mut s = String::new();
                let mut c_ = c;
                let mut has_symbol = false;
                while c_ < width && maze[r][c_].is_ascii_digit() {
                    s.push(maze[r][c_] as char);
                    has_symbol = has_symbol
                        || neighbors_2d(r, c_, &maze_s)
                            .iter()
                            .any(|(c, _, _)| issymbol(c));
                    c_ += 1;
                }
                //println!("Found number {s} counts? {has_symbol}");
                if has_symbol {
                    sum += s.parse::<i32>().unwrap();
                }
                c = c_;
                continue;
            }
            c += 1;
        }
    }
    return sum;
}

/// Finds gear ratio of number neighbors
fn find_num_neighbors(r: usize, c: usize, maze: &Maze) -> i32 {
    // Visited set to avoid double-counting e.g.
    // 233
    //   *444
    let mut visited: Vec<(i32, i32)> = Vec::new();
    // Numbers found
    let mut nums: Vec<i32> = Vec::new();
    // Check neighbors
    for (cha, r_, c_) in neighbors_2d(r, c, &maze) {
        // Skip numbers we found or non-numbers
        if !cha.is_ascii_digit() || visited.contains(&(r_, c_)) {
            continue;
        }
        // Find left extent
        let mut c__ = c_;
        while c__ >= 0 && (maze.maze[r_ as usize][c__ as usize].is_ascii_digit()) {
            c__ -= 1
        }
        c__ += 1;
        // Parse num from left extent to right, append to string and 'visited'
        let mut s = String::new();
        while (c__ < (maze.width as i32)) && (maze.maze[r_ as usize][c__ as usize].is_ascii_digit())
        {
            visited.push((r_, c__));
            s.push(maze.maze[r_ as usize][c__ as usize] as char);
            c__ += 1;
        }
        nums.push(s.parse::<i32>().unwrap());
    }
    // One case is great, less than 2 numbers is 0, and above is parse error
    return match nums[..] {
        [a, b] => a * b,
        [a] => 0,
        [] => 0,
        _ => panic!("Found {} not <= 2", nums.len()),
    };
}

fn p2(inp: &str) -> i32 {
    let maze_s = utils::load_2darr(inp);
    let Maze {
        height,
        width,
        ref maze,
    } = maze_s;
    let mut res = 0;
    for r in 0..height {
        for c in 0..width {
            let cha = maze[r][c];
            if cha != b'*' {
                continue;
            };
            // Find number neighbors
            res += find_num_neighbors(r, c, &maze_s);
        }
    }
    return res;
}
