use regex::Regex;
use std::collections::hash_map::HashMap;
use utils;

#[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
enum Spring {
    Working,
    Broken,
    Unknown,
}

fn makeSpringVec(inp: &str) -> Vec<Spring> {
    inp.chars()
        .map(|c| match c {
            '#' => Spring::Broken,
            '.' => Spring::Working,
            '?' => Spring::Unknown,
            _ => panic!("Unknown char"),
        })
        .collect()
}

fn main() {
    let inp = utils::load_input(true, "day12");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> usize {
    let redigit: Regex = Regex::new(r"\d+").unwrap();
    let re: Regex = Regex::new(r"([#.?]*) ([0-9,]*)").unwrap();
    let parsedlines: Vec<(Vec<Spring>, Vec<usize>)> = inp
        .lines()
        .map(|l| re.captures(l).expect("Couldn't match {l}"))
        .map(|c| c.extract())
        .map(|(_, [a, b])| (a, b))
        .map(|(a, b)| {
            (
                makeSpringVec(a),
                b.split(',').map(|d| d.parse::<usize>().unwrap()).collect(),
            )
        })
        .collect();
    //println!("{:?}", parsedlines);
    let mut c = 0;
    for (spr, cont) in parsedlines {
        let x = rec_(&spr, &cont);
        //println!("{:?}: {}", spr, x);
        c += x;
    }
    //println!("{:#?}", contiguous(makeSpringVec("##...#.####")));
    return c;
}

fn rec_ (sprs: &[Spring], cont: &[usize]) -> usize {
    let (x, _) = rec(sprs, cont, 0, HashMap::new());
    x
}

fn rec<'a, 'b>(sprs: &'a [Spring], cont: &'b [usize], cur: usize, map: HashMap<(&'a [Spring], &'b [usize], usize), usize>) -> (usize, HashMap<(&'a [Spring], &'b [usize], usize), usize>) {
    // Vec<Vec<Spring>> {
    match map.get(&(sprs, cont, cur)) {
        Some(x) => return (*x, map),
        None => (),
    };
    let (x, mut map_after) = match sprs.split_first() {
        Some((Spring::Broken, tail)) => {
            // Increase count
            rec(tail, cont, cur + 1, map)
        }
        Some((Spring::Working, tail)) => {
            // If we're not in a segment, thats fine
            if cur == 0 {
                rec(tail, cont, cur, map)
            } else {
                // We're at the end of a segment, verify length
                if let Some((c, cs)) = cont.split_first() {
                    if *c == cur {
                        // We ended a segment, and it was the expected length
                        rec(tail, cs, 0, map)
                    } else {
                        // We ended a segment, but it wasn't the expected length
                        (0, map)
                    }
                } else {
                    // We ended a segment, but we shouldn't have
                    // Dead-end
                    (0, map)
                }
            }
        }
        Some((Spring::Unknown, tail)) => {
            // Check if this can be a Working spring
            let (branch1, map2) = if cur == 0 {
                rec(tail, cont, cur, map)
            } else {
                if let Some((c, cs)) = cont.split_first() {
                    if *c == cur {
                        rec(tail, cs, 0, map)
                    } else {
                        (0, map)
                    }
                } else {
                    (0, map)
                }
            };
            let (branch2, map3) = rec(tail, cont, cur + 1, map2);
            (branch1 + branch2, map3)
        }
        None => match cont {
            [] => {
                if cur == 0 {
                    (1, map)
                } else {
                    (0, map)
                }
            }
            [c] => {
                if cur == *c {
                    (1, map)
                } else {
                    (0, map)
                }
            }
            _ => (0, map),
        },
    };
    map_after.insert((sprs, cont, cur), x);
    (x, map_after)

}

fn expand(sprs: Vec<Spring>, cont: Vec<usize>) -> (Vec<Spring>, Vec<usize>) {
    (
        vec![
            sprs.clone(),
            sprs.clone(),
            sprs.clone(),
            sprs.clone(),
            sprs.clone(),
        ].join(&Spring::Unknown),
        cont.repeat(5)
    )
}

fn p2(inp: &str) -> usize {
    let redigit: Regex = Regex::new(r"\d+").unwrap();
    let re: Regex = Regex::new(r"([#.?]*) ([0-9,]*)").unwrap();
    let parsedlines: Vec<(Vec<Spring>, Vec<usize>)> = inp
        .lines()
        .map(|l| re.captures(l).expect("Couldn't match {l}"))
        .map(|c| c.extract())
        .map(|(_, [a, b])| (a, b))
        .map(|(a, b)| {
            (
                makeSpringVec(a),
                b.split(',').map(|d| d.parse::<usize>().unwrap()).collect(),
            )
        })
        .collect();
    let mut c = 0;
    let mut i = 0;
    let tot = parsedlines.len();
    for (spr, cont) in parsedlines {
        let (spr_, cont_) = expand(spr, cont);
        let (x, _) = rec(&spr_, &cont_, 0, HashMap::new());
        //println!("{}/{}", i, tot);
        i += 1;
        c += x;
    }
    return c;
}

#[cfg(test)]
mod tests {
    use crate::Spring::*;
    use crate::*;

    #[test]
    pub fn simple() {
        assert_eq!(1, rec_(&[Broken, Working], &[1]));
        assert_eq!(1, rec_(&[Working, Broken], &[1]));
        assert_eq!(0, rec_(&[Working, Broken, Broken, Working], &[1]));
        assert_eq!(1, rec_(&[Working, Broken, Broken, Working], &[2]));
        assert_eq!(1, rec_(&[Working, Broken, Working, Broken], &[1, 1]));
    }
    #[test]
    pub fn simple_diverging() {
        assert_eq!(1, rec_(&[Broken, Unknown, Working], &[1]));
        assert_eq!(1, rec_(&[Broken, Unknown, Broken], &[1, 1]));
        assert_eq!(
            1,
            rec_(
                &[Unknown, Unknown, Unknown, Working, Broken, Broken, Broken],
                &[1, 1, 3])
        );
    }
    #[test]
    pub fn diverging() {
        assert_eq!(
            4,
            rec_(
                &[
                    Working, Unknown, Unknown, Working, Working, Unknown, Unknown, Working,
                    Working, Working, Unknown, Broken, Broken, Working
                ],
                &[1, 1, 3])
        );
    }
}
