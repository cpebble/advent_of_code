use regex::Regex;
use std::{iter::zip, ops::Range};
use utils;

#[allow(dead_code)]
struct Race {
    time: usize,
    distance: usize,
}

#[allow(dead_code)]
impl Race {
    pub fn new(time: usize, distance: usize) -> Race {
        Race { time, distance }
    }
}

fn main() {
    let inp = utils::load_input(true, "day6");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}

fn simrace(r: Race) -> usize {
    let (mut t, mut v, mut d) = (0, 0, 0);
    //println!("Simulating d: {}, t: {}", r.distance, r.time);
    let mut solutions = 0;

    let mut crest = false;
    loop {
        // See if we hit target
        if (r.time - t) * t > r.distance {
            solutions += 1;
            crest = true;
            //println!("Hold: {t}, time left: {}, distance: {}", r.time-t, r.time*t);
        } else if crest {
            break;
        }

        t += 1;
    }
    return solutions;
}
fn p1(inp: &str) -> i32 {
    let mut inp = inp.split("\n");
    let times: Vec<usize> = Regex::new(r"\d+")
        .unwrap()
        .find_iter(inp.next().expect("Parse err"))
        .map(|num| num.as_str().parse::<usize>().unwrap())
        .collect();
    let distances: Vec<usize> = Regex::new(r"\d+")
        .unwrap()
        .find_iter(inp.next().expect("Parse err"))
        .map(|num| num.as_str().parse::<usize>().unwrap())
        .collect();
    let i = 0;

    //println!("{:?}", utils::strvec(&times, ", "));
    let races = zip(times, distances).map(|(t, d)| Race::new(t, d));
    let results = races.map(|r| simrace(r)).collect::<Vec<usize>>();
    //println!("{:?}", utils::strvec(&results, ","));

    results.iter().fold(1, |a, e| a * (*e as i32))
}
fn p2(inp: &str) -> i32 {
    let mut inp = inp.split("\n");
    let time: usize = Regex::new(r"[ \d]+")
        .unwrap()
        .find(inp.next().expect("Unexpected EOF"))
        .expect("no numbers found")
        .as_str()
        .replace(" ", "")
        .parse::<usize>()
        .expect("Usize parse err");
    let distance: usize = Regex::new(r"[ \d]+")
        .unwrap()
        .find(inp.next().expect("Unexpected EOF"))
        .expect("no numbers found")
        .as_str()
        .replace(" ", "")
        .parse::<usize>()
        .expect("Usize parse err");
    simrace(Race { time, distance}).try_into().unwrap()

}
