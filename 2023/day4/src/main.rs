use std::collections::{HashMap, HashSet};

use regex::Regex;
use utils::{self};

static PROD: bool = true;
fn main() {
    let inp = utils::load_input(PROD, "day4");
    let part1 = p1(&inp);
    println!("Part 1: {}", part1);
    if PROD {
        assert!(part1 < 25795);
        assert!(part1 > 12887);
    } else {
        assert!(part1 == 13);
    }
    println!("Part 2: {}", p2(&inp));
}

type Cards = Vec<(i32, HashSet<i32>, Vec<i32>)>;

fn extract_cards(inp: &str) -> Cards {
    let redigit: Regex = Regex::new(r"\d+").unwrap();
    let resplit: Regex = Regex::new(r"Card +(\d*):(.*)\|(.*)").unwrap();
    inp.lines()
        .map(|l| match resplit.captures(l) {
            Some(x) => x,
            None => panic!("Couldn't match {l}"),
        })
        .map(|caps| {
            let (_, [cardid, winners, totals]) = caps.extract();
            let winvec = HashSet::from_iter(redigit.find_iter(winners).map(|w| {
                w.as_str()
                    .parse::<i32>()
                    .expect("couldn't parse {w} as i32")
            }));
            let numvec = Vec::from_iter(redigit.find_iter(totals).map(|w| {
                w.as_str()
                    .parse::<i32>()
                    .expect("couldn't parse {w} as i32")
            }));
            (
                cardid
                    .parse::<i32>()
                    .expect("Couldn't parse {cardid} as i32"),
                winvec,
                numvec,
            )
        })
        .collect()
}

fn cardscores(cards: Cards) -> HashMap<i32, (i32, i32)> {
    let mut m = HashMap::new();
    for (cid, winset, numvec) in cards {
        let valid: u32 = numvec
            .iter()
            .map(|x| if winset.contains(x) { 1 } else { 0 })
            .sum();
        let score: i32;
        if valid >= 1 {
            score = (2 as i32).pow(valid - 1)
        } else {
            score = 0
        }
        m.insert(
            cid,
            (
                valid
                    .try_into()
                    .expect("Invalid int conversion in card {cid}"),
                score,
            ),
        );
    }
    return m;
}

fn p1(inp: &str) -> i32 {
    cardscores(extract_cards(inp))
        .values()
        .map(|(_, s)| s)
        .sum()
}
fn p2(inp: &str) -> i32 {
    let cscores = cardscores(extract_cards(inp));
    let mut ccounts: HashMap<i32, i32> = HashMap::new();
    let mut sorted_keys = Vec::from_iter(cscores.keys());
    sorted_keys.sort();

    // Going through this sorted allows us to iterate only once
    for cid in sorted_keys {
        let (valid, score) = cscores.get(cid).unwrap();
        let count = *ccounts.entry(*cid).or_insert(1);
        for i in 1..=*valid {
            ccounts
                .entry(*cid + i)
                .and_modify(|c| *c += count)
                .or_insert(1 + count);
        }
    }
    // We just need to count how many cards total
    return ccounts.values().sum();
}


#[cfg(test)]
mod tests {}
