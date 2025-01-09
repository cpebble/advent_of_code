use std::collections::HashMap;

use num_integer;
use regex::Regex;
use utils;

struct Tree {
    label: String,
    left: Option<Box<Tree>>,
    right: Option<Box<Tree>>,
}
struct DTree {
    label: String,
    left: String,
    right: String,
}

impl Tree {}

fn main() {
    let inp = utils::load_input(true, "day8");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}

fn p1(inp: &str) -> usize {
    let gregex = Regex::new(r"([A-Z]*) = \(([A-Z]*), ([A-Z]*)\)").unwrap();
    let [instr, graph] = utils::load_parts(inp)[0..2] else {
        panic!("Bad input")
    };
    let mut g: HashMap<&str, DTree> = HashMap::new();
    for l in graph.lines() {
        let (_, [label, left, right]) = gregex
            .captures(l)
            .expect(&format!("{l} Didn't parse properly"))
            .extract();
        let t = DTree {
            label: label.to_string(),
            left: left.to_string(),
            right: right.to_string(),
        };
        g.insert(label, t);
    }

    let instr = instr.as_bytes();
    let start = "AAA";
    let end = "ZZZ";
    let mut cur = g.get(start).expect("We went down a bad path");
    let mut i: usize = 0;
    while cur.label != end {
        if (instr[i % instr.len()] as char) == 'L' {
            cur = g.get(cur.left.as_str()).expect("We went down a bad path");
        } else {
            cur = g.get(cur.right.as_str()).expect("We went down a bad path");
        }
        i += 1;
    }
    return i;
}
fn run(g: &HashMap<&str, DTree>, instr: &[u8], start: &str) -> usize {
    let mut cur = g.get(start).expect("We went down a bad path");
    let mut i: usize = 0;
    while !cur.label.ends_with("Z") {
        if (instr[i % instr.len()] as char) == 'L' {
            cur = g.get(cur.left.as_str()).expect("We went down a bad path");
        } else {
            cur = g.get(cur.right.as_str()).expect("We went down a bad path");
        }
        i += 1;
    }
    return i;
}
fn p2(inp: &str) -> usize {
    let gregex = Regex::new(r"([0-9A-Z]*) = \(([0-9A-Z]*), ([0-9A-Z]*)\)").unwrap();
    let [instr, graph] = utils::load_parts(inp)[0..2] else {
        panic!("Bad input")
    };
    let mut g: HashMap<&str, DTree> = HashMap::new();
    for l in graph.lines() {
        let (_, [label, left, right]) = gregex
            .captures(l)
            .expect(&format!("{l} Didn't parse properly"))
            .extract();
        let t = DTree {
            label: label.to_string(),
            left: left.to_string(),
            right: right.to_string(),
        };
        g.insert(label, t);
    }

    let instr = instr.as_bytes();
    // Check length of each run, calculate lowest_common_denominator
    g.keys()
        .filter(|k| k.ends_with("A"))
        .map(|s| run(&g, instr, &s))
        .fold(1, |acc, r| (acc * r) / num_integer::gcd(acc, r))
}

#[cfg(test)]
mod tests {
    use crate::*;

    #[test]
    fn p1example() {
        let inp = "LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)";
        assert_eq!(p1(inp), 6);
    }
    #[test]
    fn p1example_2() {
        let inp = "RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)";
        assert_eq!(p1(inp), 2);
    }
    #[test]
    fn p2_stillholds() {
        let inp = "RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)";
        assert_eq!(p2(inp), 2);
    }
    #[test]
    fn p2example() {
        let inp = "LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
";
        assert_eq!(p2(inp), 6);
    }
}
