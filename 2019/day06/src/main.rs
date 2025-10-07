use regex::Regex;
use std::collections::HashMap;
use utils;

struct Body {
    name: char,
    orbits: Box<Body>,
}

fn main() {
    let inp = utils::load_input(true, "day06");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> i32 {
    let mut orbits: HashMap<String, String> = HashMap::new();
    let re = Regex::new(r"(.*)\)(.*)").unwrap();
    for (_, [a, b]) in re.captures_iter(inp).map(|c| c.extract()) {
        orbits.insert(b.to_string(), a.to_string());
        // println!("{}>{}", a, b);
    }
    // Now find indirect orbits
    let mut directs = 0;
    let mut queue = Vec::new();
    let initial = "COM".to_string();
    queue.push((&initial, -1));
    while let Some((cur, lvl)) = queue.pop() {
        //println!("{} {} [{:?}]", cur, lvl, queue);
        let clvl = lvl + 1;
        directs += clvl;
        for (n, _) in orbits
                .iter()
                .filter(|(_, x)| *x == cur){
            queue.push((n, clvl));
        }
                //.map(|n| queue.push((n, clvl)));
    }
    directs
}
fn p2(inp: &str) -> i32 {
    let mut orbits: HashMap<String, String> = HashMap::new();
    let re = Regex::new(r"(.*)\)(.*)").unwrap();
    for (_, [a, b]) in re.captures_iter(inp).map(|c| c.extract()) {
        orbits.insert(b.to_string(), a.to_string());
    }
    let mut cur = &("YOU".to_string());
    let mut dists = HashMap::new();
    let mut i = 0;
    while cur != "COM" {
        let next = orbits.get(cur).unwrap();
        dists.insert(next, i);
        i += 1;
        cur = next;
    }
    let binding = ("SAN".to_string());
    cur = &binding;
    i = 0;
    while (!dists.contains_key(cur)) || (cur == &("COM".to_string())){
        cur = orbits.get(cur).unwrap();
        i += 1;
    }
    dists.get(cur).unwrap() + i - 1
}

mod tests {
    use crate::*;
    static TEST: &str = "COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L";
    static TEST2: &str = "COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN";

    #[test]
    fn p1example() {
        let inp = TEST;
        let target = 42;
        assert_eq!(p1(inp), target);
    }
    #[test]
    fn p2example() {
        let inp = TEST2;
        let target = 4;
        assert_eq!(p2(inp), target);
    }
}
