use regex::Regex;
use utils;

fn parseword(w: &str) -> u32 {
    match w {
        "one" => 1,
        "two" => 2,
        "three" => 3,
        "four" => 4,
        "five" => 5,
        "six" => 6,
        "seven" => 7,
        "eight" => 8,
        "nine" => 9,
        c => u32::from_str_radix(c, 10).unwrap()
    }
}

fn main() {
    let inp = utils::load_input(true, "day1");
    //print!("{}", inp);
    let mut p1 = 0;
    for l in inp.lines() {
        let mut d1: u32 = 0;
        let mut d2: u32 = 0;
        for c in l.chars() {
            if c.is_numeric() {
                d1 = c.to_digit(10).unwrap();
                break;
            }
        }
        for c in l.chars().rev() {
            if c.is_numeric() {
                d2 = c.to_digit(10).unwrap();
                break;
            }
        }
        p1 += (d1 * 10) + d2;
    }
    println!("P1: {}", p1);
    p2(inp);
}
fn p2(inp: String){
    let mut p2 = 0;
    let re: Regex = Regex::new(r"([1-9]|one|two|three|four|five|six|seven|eight|nine)").unwrap();
    for l in inp.lines() {
        let mut g2: Vec<&str> = Vec::new();
        let mut i = 0;
        loop {
            match re.find_at(l, i) {
                Some(mat) => {i = mat.start() + 1; g2.push(mat.as_str())}
                None => break,
            }
        }
        //println!("{} - {} + {}", l, (g2[0]), parseword(g2[g2.len()-1]));
        p2 += parseword(g2[0])*10 + parseword(g2[g2.len()-1]);
    }
    println!("P2: {}", p2);
    // 50480 < x < 54506
}
