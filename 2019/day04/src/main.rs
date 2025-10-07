use regex::Regex;
use utils;

const INP: &str = "264360-746325";
fn main() {
    println!("Part 1: {}", p1());
    println!("Part 2: {}", p2());
}

fn is_str_valid(pass: &str) -> bool {
    if pass.len() != 6 {
        println!("Len mismatch");
        return false;
    }
    let mut last = '/';
    let mut double = false;
    for c in pass.chars() {
        if c < last {
            return false;
        }
        if c == last {
            double = true;
        }
        last = c;
    }
    return double;
}

fn is_str_valid2(pass: &str) -> bool {
    if pass.len() != 6 {
        println!("Len mismatch");
        return false;
    }
    let mut run = 1;
    let mut double = false;
    let mut last = '/';
    for c in pass.chars() {
        if c < last {
            // println!("{:?}-{:?}", c, last);
            return false;
        }
        if c == last {
            run += 1;
        } else {
            if run == 2 {
                double = true;
            }
            run = 1;
        }
        last = c;
    }
    // println!("{:?}-{:?}", double,run);
    double || run == 2
}

fn p1() -> i32 {
    let preg = Regex::new(r"(\d*)-(\d*)").unwrap();
    let (_, [start, end]) = preg.captures(INP).expect("Yikes").extract();
    let mut count = 0;
    for i in (start.parse::<usize>().unwrap())..(end.parse::<usize>().unwrap()) {
        if is_str_valid(&format!("{:06}", i)) {
            count += 1;
        }
    }
    return count;
}
fn p2() -> i32 {
    let preg = Regex::new(r"(\d*)-(\d*)").unwrap();
    let (_, [start, end]) = preg.captures(INP).expect("Yikes").extract();
    let mut count = 0;
    for i in (start.parse::<usize>().unwrap())..(end.parse::<usize>().unwrap()) {
        if is_str_valid2(&format!("{:06}", i)) {
            count += 1;
        }
    }
    return count;
}

#[cfg(test)]
mod tests {
    use crate::*;
    #[test]
    fn p2example() {
        assert!(is_str_valid2("112233"));
        assert!(!is_str_valid2("123444"));
        assert!(is_str_valid2("111122"));
    }
}
