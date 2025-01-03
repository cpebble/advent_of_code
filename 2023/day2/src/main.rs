use regex::Regex;
use core::fmt;
use std::{collections::HashMap, cmp::max};
use utils;

fn main() {
    let inp = utils::load_input(true, "day2");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
#[derive(Eq, Hash, PartialEq, Debug)]
enum Colors {
    Red,
    Green,
    Blue,
}

impl Colors {
    fn from_str(input: &str) -> Option<Colors> {
        match input {
            "red" => Some(Colors::Red),
            "blue" => Some(Colors::Blue),
            "green" => Some(Colors::Green),
            _ => None,
        }
    }
}
impl fmt::Display for Colors {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Colors::Red =>   write!(f, "Red"),
            Colors::Green => write!(f, "Green"),
            Colors::Blue =>  write!(f, "Blue"),
        }
    }
}

fn printrec(r: &HashMap<Colors, i32>) {
    print!("{{");
    for (col, count) in r.iter() {
        print!("{}: {},", col, count);
    }
    print!(r"}}");
}

fn parsegames(inp: &str) -> HashMap<i32, HashMap<Colors, i32>> {
    let mut games: HashMap<i32, HashMap<Colors, i32>> = HashMap::new();
    for l in inp.lines() {
        let mut record: HashMap<Colors, i32> = HashMap::new();
        let (mut r, mut g, mut b) = (0, 0, 0);
        let (_, [gameid]) = Regex::new(r"Game (\d+)")
            .unwrap()
            .captures_iter(l)
            .next()
            .unwrap()
            .extract();
        for x in Regex::new(r"(\d+) ([a-z]+)").unwrap().captures_iter(l) {
            let (_, [count, color]) = x.extract();
            let col = Colors::from_str(color).unwrap();
            match col {
                Colors::Red => r = max(r, i32::from_str_radix(count, 10).unwrap()),
                Colors::Green => g = max(g, i32::from_str_radix(count, 10).unwrap()),
                Colors::Blue => b =  max(b, i32::from_str_radix(count, 10).unwrap()), 
            };
        }
        record.insert(Colors::Red, r);
        record.insert(Colors::Green, g);
        record.insert(Colors::Blue, b);
        games.insert(i32::from_str_radix(gameid, 10).unwrap(), record);
    }
    return games;
}

fn p1(inp: &str) -> i32 {
    let games = parsegames(inp);
    let mut sum = 0;
    let (maxr, maxg, maxb) = (12, 13, 14);
    for (game, record) in games.iter() {
        if record.get(&Colors::Red).unwrap() <= &maxr &&
           record.get(&Colors::Green).unwrap() <= &maxg &&
           record.get(&Colors::Blue).unwrap() <= &maxb{
            sum += game;
            //println!("Game {} Valid", game);
        }
        else{
            //println!("Game {} INValid", game);
            //printrec(record);
            //println!("");

        }
    }
    return sum;
}
fn p2(inp: &str) -> i32 {
    let games = parsegames(inp);
    let mut sum = 0;
    for (game, record) in games.iter() {
        let r = record.get(&Colors::Red).unwrap();
        let g = record.get(&Colors::Green).unwrap();
        let b = record.get(&Colors::Blue).unwrap();
        sum += r*g*b;
    }
    return sum;
}
