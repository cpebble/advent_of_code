use utils;
use utils::Tile;

type Maze = utils::IMaze<Tile>;

fn main() {
    let inp = utils::load_input(false, "day14");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}

fn shiftNorth(m_: Maze) -> Maze {
    let mut m = m_.clone();
    for c in 0..m.width {
        let mut cur = 0;
        for r in 0..m.height {
            match m_.maze[r][c] {
                Tile::Hash => cur = r + 1,
                Tile::Dot => {}
                Tile::Round => {
                    m.maze[r][c] = Tile::Dot;
                    m.maze[cur][c] = Tile::Round;
                    cur += 1;
                }
                _ => (),
            }
        }
    }
    return m;
}
fn shift_north_m(mut m_: Maze) -> Maze {
    for c in 0..m_.width {
        let mut cur = 0;
        for r in 0..m_.height {
            match m_.maze[r][c] {
                Tile::Hash => cur = r + 1,
                Tile::Dot => {}
                Tile::Round => {
                    m_.maze[r][c] = Tile::Dot;
                    m_.maze[cur][c] = Tile::Round;
                    cur += 1;
                }
                _ => (),
            }
        }
    }
    return m_;
}
fn shift_south_m(mut m_: Maze) -> Maze {
    for c in 0..m_.width {
        let mut cur = m_.height - 1;
        for r in (0..m_.height).rev() {
            match m_.maze[r][c] {
                Tile::Hash => cur = if r != 0 { r - 1 } else { 0 },
                Tile::Dot => {}
                Tile::Round => {
                    m_.maze[r][c] = Tile::Dot;
                    m_.maze[cur][c] = Tile::Round;
                    cur -= if r != 0 { 1 } else { 0 };
                }
                _ => (),
            }
        }
    }
    return m_;
}
fn shift_west_m(mut m_: Maze) -> Maze {
    for r in 0..m_.height {
        let mut cur = 0;
        for c in 0..m_.width {
            match m_.maze[r][c] {
                Tile::Hash => cur = c + 1,
                Tile::Dot => {}
                Tile::Round => {
                    m_.maze[r][c] = Tile::Dot;
                    m_.maze[r][cur] = Tile::Round;
                    cur += 1;
                }
                _ => (),
            }
        }
    }
    return m_;
}
fn shift_east_m(mut m_: Maze) -> Maze {
    for r in 0..m_.height {
        let mut cur = m_.width - 1;
        for c in (0..m_.width).rev() {
            match m_.maze[r][c] {
                Tile::Hash => cur -= if c != 0 { 1 } else { 0 },
                Tile::Dot => {}
                Tile::Round => {
                    m_.maze[r][c] = Tile::Dot;
                    m_.maze[r][cur] = Tile::Round;
                    cur -= if c != 0 { 1 } else { 0 };
                }
                _ => (),
            }
        }
    }
    return m_;
}

fn p1(inp: &str) -> i32 {
    let m: Maze = utils::load_2darr(inp).into();
    //println!("{}", m.to_str());

    let m2 = shiftNorth(m);
    //println!("{}", m2.to_str());
    return load(m2).try_into().unwrap();
}

fn load(m: Maze) -> usize {
    m.into_iter()
        .map(|(r, c, t)| match t {
            Tile::Round => m.height - r,
            _ => 0,
        })
        .sum()
}
fn p2(inp: &str) -> i32 {
    let mut m: Maze = utils::load_2darr(inp).into();
    for c in 0..1000000000 {
        if c == 0 {
            m = shift_north_m(m);
            println!("{}", m.to_str());
            m = shift_east_m(m);
            println!("{}", m.to_str());
            m = shift_south_m(m);
            println!("{}", m.to_str());
            m = shift_west_m(m);
            println!("{}", m.to_str());
        } else {
            m = shift_west_m(shift_south_m(shift_east_m(shift_north_m(m))));
            if c <= 3 {
                println!("After {} Cycles: \n{}", c, m.to_str());
            }
        }
    }
    return load(m).try_into().unwrap();
}

#[cfg(test)]
mod tests {
    use crate::*;
    #[test]
    pub fn testmnorth() {
        let m: Maze = utils::load_2darr(
            "\
O...
.#OO
..#.
OO#O",
        )
        .into();
        let m2 = shift_north_m(m);
        println!("{}", m2.to_str());
        assert_eq!(
            m2.to_str(),
            "\
O.OO
O#.O
.O#.
..#.
"
        );
        let m3 = shift_south_m(m2);
        println!("{}", m3.to_str());
        assert_eq!(
            m3.to_str(),
            "\
....
.#O.
O.#O
OO#O
"
        );
    }

    // Here
    #[test]
    pub fn testmeast() {
        let m: Maze = utils::load_2darr(
            "\
O...
.#OO
..#.
OO#O",
        )
        .into();
        let m2 = shift_east_m(m);
        println!("{}", m2.to_str());
        assert_eq!(
            m2.to_str(),
            "\
...O
.#OO
..#.
OO#O
"
        );
        let m3 = shift_west_m(m2);
        assert_eq!(
            m3.to_str(),
            "\
O...
.#OO
..#.
OO#O
"
        );
    }
}
