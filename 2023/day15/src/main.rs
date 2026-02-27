use core::array;
use regex;
use std::fmt;
use utils;

fn main() {
    let inp = utils::load_input(true, "day15");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> i32 {
    let strs = parseInput(inp);
    strs.into_iter().map(hash).fold(0, |a, e| a + (e as i32))
}
fn p2(inp: &str) -> i32 {
    let strs = parseInput(inp);
    let mut map: [Vec<(&str, u8)>; 256] = array::from_fn(|_| Vec::new());
    for s in strs {
        let pos = s.find(|c| c == '-' || c == '=').unwrap();
        let (label, op) = (&s[0..pos], s.chars().nth(pos).unwrap());
        let ind = hash(label);
        let bx = &mut map[ind as usize];
        match op {
            '-' => drop(bx, label),
            '=' => {
                let val = (s.chars().nth(pos + 1).unwrap() as u8) - 48;
                change(&mut map[ind as usize], label, val);
            }
            c => panic!("[{s}Unknown char {c}"),
        }
    }
    println!("After :\n{}", print_box(&map));
    return checksum(&map);
}

fn print_box(bx: &[Vec<(&str, u8)>; 256]) -> String {
    let mut out = String::new();
    for i in 0..256 {
        if bx[i].len() != 0 {
            out.push_str(format!("Box {i}: {:?}\n", bx[i]).as_str());
        }
    }
    return out;
}

fn drop<'a>(bx: &mut Vec<(&'a str, u8)>, lab: &'a str) {
    for j in 0..bx.len() {
        if bx[j].0 == lab {
            bx.remove(j);
            return;
        }
    }
}

fn change<'a>(bx: &mut Vec<(&'a str, u8)>, lab: &'a str, new: u8) {
    for i in 0..bx.len() {
        if bx[i].0 == lab {
            bx[i] = (lab, new);
            return;
        }
    }
    bx.push((lab, new))
}

fn hash(txt: &str) -> u8 {
    let mut curval: usize = 0;
    for c in txt.chars() {
        curval = ((curval + (c as usize)) * 17) % 256;
    }
    curval as u8
}

fn checksum(map: &[Vec<(&str, u8)>; 256]) -> i32 {
    let mut c: i32 = 0;
    for i in 0..256 {
        for j in 0..map[i].len() {
            let chk: i32 = ((i+1)*(j+1)*(map[i][j].1 as usize)).try_into().unwrap();
            c += chk;
        }
    }
    c
}

fn parseInput(inp: &str) -> Vec<&str> {
    inp.strip_suffix('\n').unwrap_or(inp).split(",").collect()
}

#[cfg(test)]
mod tests {
    use crate::*;
    #[test]
    pub fn testhash() {
        assert_eq!(hash("HASH"), 52);
    }
}
