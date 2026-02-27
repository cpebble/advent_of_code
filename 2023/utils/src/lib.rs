use regex::Regex;
use std::fmt::Display;
use std::fs::File;
use std::io::Read;
use std::path::Path;

//static PROD: bool = false;
//static DAY: &str = "day1";
pub fn load_input(prod: bool, day: &str) -> String {
    let path: String = match prod {
        true => format!("inputs/{}.input", day),
        false => format!("inputs/{}.example", day),
    };
    let mut file = match File::open(Path::new(&path)) {
        Ok(s) => s,
        Err(why) => panic!("Error in reading {path}\n{why}\n"),
    };
    let mut out = String::new();
    match file.read_to_string(&mut out) {
        Ok(_) => (),
        Err(why) => panic!("BBBBBBBBB {}\n", why),
    }
    return out;
}

#[derive(Eq, PartialEq, Hash)]
pub struct IMaze<A> {
    pub height: usize,
    pub width: usize,
    pub maze: Vec<Vec<A>>,
}

pub type Maze = IMaze<u8>;

impl From<IMaze<u8>> for IMaze<Tile> {
    fn from(value: IMaze<u8>) -> Self {
        let mut m = Vec::new();

        for r in 0..value.height {
            let mut rv = Vec::new();
            for c in 0..value.width {
                rv.push((value.maze[r][c] as char).into());
            }
            m.push(rv)
        }
        IMaze {
            height: value.height,
            width: value.width,
            maze: m,
        }
    }
}

impl IMaze<u8> {
    pub fn to_str(&self) -> String {
        let mut out = String::new();
        for r in 0..self.height {
            for c in 0..self.width {
                out.push(self.maze[r][c].clone() as char);
            }
            out.push('\n');
        }
        out
    }
}
impl IMaze<Tile> {
    pub fn to_str(&self) -> String {
        let mut out = String::new();
        for r in 0..self.height {
            for c in 0..self.width {
                out.push(self.maze[r][c].clone().into());
            }
            out.push('\n');
        }
        out
    }
}
impl<A: Clone> Clone for IMaze<A> {
    fn clone(&self) -> Self {
        Self {
            height: self.height.clone(),
            width: self.width.clone(),
            maze: self.maze.clone(),
        }
    }
}

pub struct MazeIter<'a, A> {
    maze: &'a IMaze<A>,
    r: usize,
    c: usize,
    started: bool,
}
impl<'a, A> MazeIter<'a, A> {
    pub fn new(m: &'a IMaze<A>) -> MazeIter<'a, A> {
        MazeIter {
            maze: m,
            r: 0,
            c: 0,
            started: false,
        }
    }
}
impl<'a, A: Copy> Iterator for MazeIter<'a, A> {
    type Item = (usize, usize, A);

    fn next(&mut self) -> Option<Self::Item> {
        if !self.started {
            self.started = true;
            return Some((self.r, self.c, self.maze.maze[self.r][self.c]));
        }
        self.c += 1;
        if self.c == self.maze.width {
            self.c = 0;
            self.r += 1;
        }
        if self.r == self.maze.height {
            None
        } else {
            Some((self.r, self.c, self.maze.maze[self.r][self.c]))
        }
    }
}

impl<'a, A: Copy> IntoIterator for &'a IMaze<A> {
    type Item = (usize, usize, A);

    type IntoIter = MazeIter<'a, A>;

    fn into_iter(self) -> Self::IntoIter {
        MazeIter::new(&self)
    }
}


#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
pub enum Tile {
    Hash,
    Dot,
    QMark,
    Round,
}
impl From<char> for Tile {
    fn from(value: char) -> Self {
        match value {
            '#' => Tile::Hash,
            '.' => Tile::Dot,
            '?' => Tile::QMark,
            'O' => Tile::Round,
            _ => todo!(),
        }
    }
}

impl Into<char> for Tile {
    fn into(self: Tile) -> char {
        match self {
            Tile::Hash => '#',
            Tile::Dot => '.',
            Tile::QMark => '?',
            Tile::Round => 'O'
        }
    }
}


pub fn load_parts(inp: &str) -> Vec<&str> {
    inp.split("\n\n").collect()
}

pub fn parse_numbers(inp: &str) -> Vec<isize> {
    let numregex = Regex::new(r"(-?\d+)").unwrap();
    numregex
        .captures_iter(inp)
        .map(|c| {
            let (_, [num]) = c.extract();
            num
        })
        .map(|c| {
            c.parse::<isize>()
                .expect(&format!("Couldn't parse '{}' as isize", c))
        })
        .collect()
}

/// Returns: Height, width, vecvec
pub fn load_2darr(inp: &str) -> Maze {
    let height: usize = inp.lines().count();
    let width: usize = inp.lines().next().unwrap().len();
    let mut arr: Vec<Vec<u8>> = Vec::new();
    for l in inp.lines() {
        arr.push(Vec::from(l));
    }
    return Maze {
        height,
        width,
        maze: arr,
    };
}
pub const COMPASS_DIRECTIONS: [(i32, i32); 4] = [(-1, 0), (0, 1), (1, 0), (0, -1)];
pub const GRID_DIRECTIONS: [(i32, i32); 8] = [
    (-1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
    (1, 0),
    (1, -1),
    (0, -1),
    (-1, -1),
];
pub fn neighbors_2d(r: usize, c: usize, maze: &Maze) -> Vec<(u8, i32, i32)> {
    let w = maze.width as i32;
    let h = maze.height as i32;
    let mut neigbors: Vec<(u8, i32, i32)> = Vec::new();
    for (dy, dx) in GRID_DIRECTIONS.iter() {
        let (nr, nc) = ((r as i32) + dy, (c as i32) + dx);
        if 0 <= nr && nr < h && 0 <= nc && nc < w {
            neigbors.push((maze.maze[nr as usize][nc as usize], nr, nc));
        }
    }
    return neigbors;
}

pub fn manhattan_distance(a: (usize, usize), b: (usize, usize)) -> usize {
    let (ar, ac) = a;
    let (br, bc) = b;
    let dr = if ar > br { ar - br } else { br - ar };
    let dc = if ac > bc { ac - bc } else { bc - ac };
    dr + dc
}

pub fn strvec<A>(arr: &Vec<A>, sep: &str) -> String
where
    A: Display,
{
    let mut s = String::new();
    for i in 0..arr.len() {
        s.push_str(arr[i].to_string().as_str());
        if i != arr.len() - 1 {
            s.push_str(sep)
        }
    }
    return s;
}

#[cfg(test)]
mod tests {

    #[test]
    fn it_works() {
        assert_eq!(4, 4);
    }
}
