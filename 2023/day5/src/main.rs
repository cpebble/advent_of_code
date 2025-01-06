use std::{collections::HashMap, fmt::Display, ops::Range};

use regex::Regex;
use utils;

/// Brute forced solution! Beware
/// runs in about a second with release build
fn main() {
    let inp = utils::load_input(true, "day5");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2smarter(&inp));
}

#[derive(PartialEq, Eq, Hash, Debug)]
enum Categories {
    Fertilizer,
    Humidity,
    Light,
    Location,
    Seed,
    Soil,
    Temperature,
    Water,
}
impl Display for Categories {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let catstr = match self {
            Categories::Fertilizer => "Fertilizer",
            Categories::Humidity => "Humidity",
            Categories::Light => "Light",
            Categories::Location => "Location",
            Categories::Seed => "Seed",
            Categories::Soil => "Soil",
            Categories::Temperature => "Temperature",
            Categories::Water => "Water",
        };
        write!(f, "{catstr}")
    }
}
fn str_to_cat(inp: &str) -> Option<Categories> {
    match inp {
        "fertilizer" => Some(Categories::Fertilizer),
        "humidity" => Some(Categories::Humidity),
        "light" => Some(Categories::Light),
        "location" => Some(Categories::Location),
        "seed" => Some(Categories::Seed),
        "soil" => Some(Categories::Soil),
        "temperature" => Some(Categories::Temperature),
        "water" => Some(Categories::Water),
        _ => None,
    }
}

// Started working on this... brute force runs in 40 minutes
// Didn't bother finishing
#[allow(dead_code)]
#[derive(Copy, Clone)]
struct SRange {
    start: i64,
    length: i64,
    end: i64,
}
#[allow(dead_code)]
impl SRange {
    pub fn new(start: i64, length: i64) -> SRange {
        SRange {
            start,
            length,
            end: start + length,
        }
    }
    pub fn newend(start: i64, end: i64) -> SRange {
        assert!(end > start);
        SRange {
            start,
            length: end - start,
            end,
        }
    }
    pub fn overlap(&self, x: &SRange) -> Option<SRange> {
        if x.start < self.start {
            x.overlap(self)
        } else if x.start > self.end {
            None
        } else {
            let start = x.start;
            let end = i64::min(self.end, x.end);
            Some(SRange::newend(x.start, i64::min(self.end, x.end)))
        }
    }
    pub fn split(&self, x: &SRange) -> Vec<SRange> {
        let Some(overlap) = self.overlap(x) else {
            return vec![self.clone()];
        };
        let mut out = Vec::new();
        if overlap.start > self.start {
            out.push(SRange::newend(self.start, overlap.start));
        }
        out.push(SRange::newend(overlap.start, overlap.end));
        if overlap.end < self.end {
            out.push(SRange::newend(overlap.end, self.end));
        }
        return out;
    }
}

struct EchoMap {
    ranges: Vec<(i64, i64, i64)>,
}
impl EchoMap {
    pub fn new() -> EchoMap {
        EchoMap { ranges: Vec::new() }
    }
    pub fn get(&self, x: i64) -> i64 {
        for (src, dst, len) in self.ranges.iter() {
            if x >= *src && x < *src + *len {
                return (x - src) + dst;
            }
        }
        return x;
    }
    pub fn bind_range(&mut self, xstart: i64, ystart: i64, range: i64) -> () {
        self.ranges.push((xstart, ystart, range))
    }
    pub fn get_inv(&self, y: i64) -> i64 {
        for (src, dst, len) in self.ranges.iter() {
            if y >= *dst && y < dst + len {
                return (y - dst) + src;
            }
        }
        return y;
    }
}

type MMap = HashMap<(Categories, Categories), EchoMap>;

fn make_maps(inp: &str) -> MMap {
    let parts = utils::load_parts(inp);
    let mapre = Regex::new(r"([a-z]+)-to-([a-z]+)").unwrap();
    let rangere = Regex::new(r"(\d*) (\d*) (\d*)").unwrap();
    //let mut mmap: MMap = HashMap::new();
    parts[1..]
        .iter()
        .map(|p| p.lines().collect::<Vec<&str>>())
        .map(|part| {
            // First find out our header
            let (_, [src, dst]) = mapre
                .captures(part[0])
                .expect("Unable to parse map header")
                .extract();
            let cfrom = str_to_cat(src).expect("{src} isn't a valid cat");
            let cto = str_to_cat(dst).expect(&format!("{dst} isn't a valid cat"));
            // Make an echomap, and bind the ranges we found
            let mut em = EchoMap::new();
            for l in part {
                let Some(caps) = rangere.captures(l) else {
                    continue;
                };
                let (_, [y, x, z]) = caps.extract();
                em.bind_range(x.parse().unwrap(), y.parse().unwrap(), z.parse().unwrap())
            }
            ((cfrom, cto), em)
        })
        .collect()
}

fn p1(inp: &str) -> i64 {
    // Parse which seeds to look at
    let seeds = Regex::new(r"(\d+)")
        .unwrap()
        .find_iter(inp.lines().next().unwrap())
        .map(|c| c.as_str())
        .map(|s| {
            s.parse::<i64>()
                .expect(&format!("{s} Couldn't be parsed as i64"))
        })
        .collect::<Vec<i64>>();
    println!("Checking seeds {:?}", seeds);
    // Make maps
    let mmap = make_maps(inp);

    println!("Running pipeline");
    let pipeline = vec![
        mmap.get(&(Categories::Seed, Categories::Soil)).unwrap(),
        mmap.get(&(Categories::Soil, Categories::Fertilizer))
            .unwrap(),
        mmap.get(&(Categories::Fertilizer, Categories::Water))
            .unwrap(),
        mmap.get(&(Categories::Water, Categories::Light)).unwrap(),
        mmap.get(&(Categories::Light, Categories::Temperature))
            .unwrap(),
        mmap.get(&(Categories::Temperature, Categories::Humidity))
            .unwrap(),
        mmap.get(&(Categories::Humidity, Categories::Location))
            .unwrap(),
    ];
    seeds
        .iter()
        .map(|s| pipeline.iter().fold(*s, |acc, el| el.get(acc)))
        .min()
        .unwrap()
}

//  Seed number 79 corresponds to soil number 81.
//  Seed number 14 corresponds to soil number 14.
//  Seed number 55 corresponds to soil number 57.
//  Seed number 13 corresponds to soil number 13.

#[allow(dead_code)]
fn p2(inp: &str) -> i64 {
    // Parse which seeds to look at
    let seedranges = Regex::new(r"\d+")
        .unwrap()
        .find_iter(inp.lines().next().unwrap())
        .map(|c| c.as_str())
        .map(|s| {
            s.parse::<i64>()
                .expect(&format!("{s} Couldn't be parsed as i64"))
        })
        .collect::<Vec<i64>>();

    // Make maps
    let mmap = make_maps(inp);

    println!("Running pipeline");
    let pipeline = vec![
        mmap.get(&(Categories::Seed, Categories::Soil)).unwrap(),
        mmap.get(&(Categories::Soil, Categories::Fertilizer))
            .unwrap(),
        mmap.get(&(Categories::Fertilizer, Categories::Water))
            .unwrap(),
        mmap.get(&(Categories::Water, Categories::Light)).unwrap(),
        mmap.get(&(Categories::Light, Categories::Temperature))
            .unwrap(),
        mmap.get(&(Categories::Temperature, Categories::Humidity))
            .unwrap(),
        mmap.get(&(Categories::Humidity, Categories::Location))
            .unwrap(),
    ];
    let mut min = i64::MAX;
    let mut i = 0;
    while i < seedranges.len() {
        let (start, range) = (seedranges[i], seedranges[i + 1]);
        let smallest = Range {
            start,
            end: start + range,
        }
        .into_iter()
        .map(|s| pipeline.iter().fold(s, |acc, el| el.get(acc)))
        .min()
        .unwrap();
        if smallest <= min {
            min = smallest;
        }
        i += 2;
    }
    return min;
}
fn p2smarter(inp: &str) -> i64 {
    // Parse which seeds to look at
    let seeds = Regex::new(r"\d+")
        .unwrap()
        .find_iter(inp.lines().next().unwrap())
        .map(|c| c.as_str())
        .map(|s| {
            s.parse::<i64>()
                .expect(&format!("{s} Couldn't be parsed as i64"))
        })
        .collect::<Vec<i64>>();

    // Make maps
    let mmap = make_maps(inp);

    println!("Running pipeline");
    let mut pipeline = vec![
        mmap.get(&(Categories::Seed, Categories::Soil)).unwrap(),
        mmap.get(&(Categories::Soil, Categories::Fertilizer))
            .unwrap(),
        mmap.get(&(Categories::Fertilizer, Categories::Water))
            .unwrap(),
        mmap.get(&(Categories::Water, Categories::Light)).unwrap(),
        mmap.get(&(Categories::Light, Categories::Temperature))
            .unwrap(),
        mmap.get(&(Categories::Temperature, Categories::Humidity))
            .unwrap(),
        mmap.get(&(Categories::Humidity, Categories::Location))
            .unwrap(),
    ];
    pipeline.reverse();
    let mut i = 0;
    let mut seedranges = Vec::new();
    while i < seeds.len() {
        let (start, range) = (seeds[i], seeds[i + 1]);
        seedranges.push(Range {
            start,
            end: start + range,
        });
        i += 2;
    }
    for i in 1..600279879{
        let x = pipeline.iter().fold(i, |acc, el| el.get_inv(acc));
        if seedranges.iter().any(|sr| sr.contains(&x)){
            return i
        }
    }
    return -1;
}
