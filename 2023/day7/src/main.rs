use std::{
    cmp::{max, Ordering},
    ops::Range,
};

use regex::Regex;
use utils;

fn main() {
    let inp = utils::load_input(true, "day7");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord)]
#[allow(dead_code)]
enum PokerHand {
    High,
    OneP,
    TwoP,
    ThreeK,
    FullH,
    FourK,
    FiveK,
}

impl PokerHand {
    pub fn get_best_no(cs: [Card; 5]) -> Option<PokerHand> {
        let mut highest = 0;
        let mut pairs = 0;
        for i in 0..5 {
            if cs[i] == Joker {
                continue;
            }
            let c = ((0 as usize)..5)
                .filter(|j| *j != i)
                .filter(|j| cs[*j] == cs[i])
                .count();
            highest = max(highest, c + 1);
            if c == 1 {
                pairs += 1;
            }
        }
        let jokers = cs.iter().filter(|c| *c == &Joker).count();
        pairs = pairs / 2;
        //println!("{} {} {}", highest, pairs, jokers);
        match (highest, pairs, jokers) {
            (5, _, _) => Some(PokerHand::FiveK),
            (4, _, 1) => Some(PokerHand::FiveK),
            (3, _, 2) => Some(PokerHand::FiveK),
            (2, _, 3) => Some(PokerHand::FiveK),
            (1, _, 4) => Some(PokerHand::FiveK),
            (0, _, 5) => Some(PokerHand::FiveK),

            (4, _, _) => Some(PokerHand::FourK),
            (3, _, 1) => Some(PokerHand::FourK),
            (2, _, 2) => Some(PokerHand::FourK),
            (1, _, 3) => Some(PokerHand::FourK),

            (2, 2, 1) => Some(PokerHand::FullH),
            (3, 1, 0) => Some(PokerHand::FullH),

            (3, 0, 0) => Some(PokerHand::ThreeK),
            (1, _, 2) => Some(PokerHand::ThreeK),

            (2, 2, 0) => Some(PokerHand::TwoP),
            (2, 1, 1) => Some(PokerHand::TwoP),

            (2, 1, 0) => Some(PokerHand::OneP),
            (1, _, 1) => Some(PokerHand::OneP),

            (1, _, 0) => Some(PokerHand::High),
            _ => None,
        }
    }
    pub fn get_best(cs: [Card; 5]) -> Option<PokerHand> {
        let mut highest = 0;
        let mut pairs = 0;
        for i in 0..5 {
            if cs[i] == Joker {
                continue;
            }
            let c = ((0 as usize)..5)
                .filter(|j| *j != i)
                .filter(|j| cs[*j] == cs[i])
                .count();
            highest = max(highest, c + 1);
            if c == 1 {
                pairs += 1;
            }
        }
        let jokers = cs.iter().filter(|c| *c == &Joker).count();
        pairs = pairs / 2;
        if jokers > 0{
            if highest == 2 {
                pairs -= 1;
            }
            if highest == 1 && jokers == 1{
                pairs += 1;
            }

            highest += jokers;
        }
        
        //println!("{} {} {}", highest, pairs, jokers);
        match (highest, pairs) {
            (5, _) => Some(PokerHand::FiveK),
            (4, _) => Some(PokerHand::FourK),
            (3, 2) => Some(PokerHand::FullH),
            (3, 1) => Some(PokerHand::FullH),
            (3, _) => Some(PokerHand::ThreeK),
            (2, 2) => Some(PokerHand::TwoP),
            (2, _) => Some(PokerHand::OneP),
            (1, _) => Some(PokerHand::High),
            _ => None,
        }
    }
}

#[derive(Debug, PartialEq, Eq, PartialOrd, Ord, Clone, Copy)]
#[allow(dead_code)]
enum Card {
    Joker,
    N2,
    N3,
    N4,
    N5,
    N6,
    N7,
    N8,
    N9,
    T,
    J,
    Q,
    K,
    A,
}

use Card::*;
impl Card {
    pub fn score(self) -> usize {
        match self {
            Card::A => 14,
            Card::K => 13,
            Card::Q => 12,
            Card::J => 11,
            Card::T => 10,
            Card::N9 => 9,
            Card::N8 => 8,
            Card::N7 => 7,
            Card::N6 => 6,
            Card::N5 => 5,
            Card::N4 => 4,
            Card::N3 => 3,
            Card::N2 => 2,
            Card::Joker => 1,
        }
    }
    pub fn from_char(c: char) -> Card {
        match c {
            'A' => Card::A,
            'K' => Card::K,
            'Q' => Card::Q,
            'J' => Card::J,
            'T' => Card::T,
            '9' => Card::N9,
            '8' => Card::N8,
            '7' => Card::N7,
            '6' => Card::N6,
            '5' => Card::N5,
            '4' => Card::N4,
            '3' => Card::N3,
            '2' => Card::N2,
            _ => panic!("Unexpected char in input"),
        }
    }
    pub fn from_char_with_joker(c: char) -> Card {
        match c {
            'A' => Card::A,
            'K' => Card::K,
            'Q' => Card::Q,
            'J' => Card::Joker,
            'T' => Card::T,
            '9' => Card::N9,
            '8' => Card::N8,
            '7' => Card::N7,
            '6' => Card::N6,
            '5' => Card::N5,
            '4' => Card::N4,
            '3' => Card::N3,
            '2' => Card::N2,
            _ => panic!("Unexpected char in input"),
        }
    }
}

#[derive(Debug)]
struct Hand {
    handstr: String,
    hand: [Card; 5],
    bid: usize,
    phand: Option<PokerHand>,
}
impl Hand {
    pub fn new(line: &str) -> Hand {
        let handregex: Regex = Regex::new(r"([AKQJTN98765432]{5}) (\d*)").unwrap();
        let (_, [cardstr, bid]) = handregex
            .captures(line)
            .expect("Couldn't parse hands")
            .extract();
        let handstr = cardstr.to_owned();
        let tmp_hand = handstr
            .chars()
            .map(|c| Card::from_char(c))
            .collect::<Vec<Card>>();
        assert!(tmp_hand.len() == 5);
        let mut hand = [N2, N2, N2, N2, N2];
        for i in 0..5 {
            hand[i] = tmp_hand[i];
        }
        let bid = bid.parse::<usize>().expect("Couldn't parse  bid");
        let phand = PokerHand::get_best(hand);
        Hand {
            handstr,
            hand,
            bid,
            phand,
        }
    }
    pub fn new_with_joker(line: &str) -> Hand {
        let handregex: Regex = Regex::new(r"([AKQJTN98765432]{5}) (\d*)").unwrap();
        let (_, [cardstr, bid]) = handregex
            .captures(line)
            .expect("Couldn't parse hands")
            .extract();
        let handstr = cardstr.to_owned();
        let tmp_hand = handstr
            .chars()
            .map(|c| Card::from_char_with_joker(c))
            .collect::<Vec<Card>>();
        assert!(tmp_hand.len() == 5);
        let mut hand = [N2, N2, N2, N2, N2];
        for i in 0..5 {
            hand[i] = tmp_hand[i];
        }
        let bid = bid.parse::<usize>().expect("Couldn't parse  bid");
        let phand = PokerHand::get_best(hand);
        Hand {
            handstr,
            hand,
            bid,
            phand,
        }
    }
    pub fn cmp(&self, other: &Hand) -> Ordering {
        let Some(h1) = &(self.phand) else {
            println!("Encountered non-good cmp between {} and {}", self.handstr, other.handstr);
            panic!("Invalid Phand Cmp")
        };
        let Some(h2) = &(other.phand) else {
            println!("Encountered non-good cmp between {} and {}", self.handstr, other.handstr);
            panic!("Invalid Phand Other")
        };
        if h1 > h2 {
            Ordering::Greater
        } else if h1 < h2 {
            Ordering::Less
        } else {
            // Need more info
            for i in 0..self.hand.len() {
                if self.hand[i] > other.hand[i] {
                    return Ordering::Greater;
                }
                if self.hand[i] < other.hand[i] {
                    return Ordering::Less;
                }
            }
            Ordering::Equal
        }
    }
}

fn p1(inp: &str) -> usize {
    let mut game = inp
        .lines()
        .map(|hline| Hand::new(hline))
        .collect::<Vec<Hand>>();
    game.sort_by(|a, b| a.cmp(b));
    //println!("{:?}", game);
    let mut sum = 0;
    for i in 0..game.len() {
        //println!("Rank: {i}, {:?}", game[i]);
        sum += game[i].bid * (i + 1)
    }
    assert_eq!(sum, 247815719);
    sum
}
fn p2(inp: &str) -> usize {
    let mut game = inp
        .lines()
        .map(|hline| Hand::new_with_joker(hline))
        .collect::<Vec<Hand>>();
    game.sort_by(|a, b| a.cmp(b));
    //println!("{:?}", game);
    let mut sum = 0;
    for i in 0..game.len() {
        //println!("Rank: {i}, {:?}", game[i]);
        sum += game[i].bid * (i + 1)
    }
    assert!(sum < 250233116);
    assert!(sum < 249043825);
    assert!(sum > 248594960);
    assert_eq!(sum, 248747492);
    sum
}

#[cfg(test)]
mod tests {
    use std::cmp::Ordering;

    use crate::Card;
    use crate::{Card::*, Hand, PokerHand};
    #[test]
    fn it_works() {
        assert!(Card::A > Card::K);
        assert!(Card::N2 < Card::T);
        assert!(Card::N2 == Card::N2);
    }
    #[test]
    fn calc_hands() {
        assert_eq!(PokerHand::get_best([A, A, A, A, A]), Some(PokerHand::FiveK));
        assert_eq!(PokerHand::get_best([A, A, A, A, K]), Some(PokerHand::FourK));
        assert_eq!(PokerHand::get_best([K, A, A, A, A]), Some(PokerHand::FourK));
        assert_eq!(PokerHand::get_best([K, A, A, A, K]), Some(PokerHand::FullH));
        assert_eq!(
            PokerHand::get_best([J, A, A, A, K]),
            Some(PokerHand::ThreeK)
        );
        assert_eq!(PokerHand::get_best([J, A, J, A, K]), Some(PokerHand::TwoP));
        assert_eq!(PokerHand::get_best([J, A, J, Q, K]), Some(PokerHand::OneP));
        assert_eq!(PokerHand::get_best([J, A, T, Q, K]), Some(PokerHand::High));
        assert_eq!(PokerHand::TwoP, PokerHand::TwoP);
    }
    #[test]
    fn calc_joker_hands() {
        assert_eq!(PokerHand::get_best([A, A, A, A, A]), Some(PokerHand::FiveK));
        assert_eq!(PokerHand::get_best([A, A, A, A, K]), Some(PokerHand::FourK));
        assert_eq!(
            PokerHand::get_best([A, A, A, A, Joker]),
            Some(PokerHand::FiveK)
        );
        assert_eq!(PokerHand::get_best([K, A, A, A, A]), Some(PokerHand::FourK));
        assert_eq!(PokerHand::get_best([K, A, A, A, K]), Some(PokerHand::FullH));
        assert_eq!(
            PokerHand::get_best([Joker, A, A, A, K]),
            Some(PokerHand::FourK)
        );
        assert_eq!(
            PokerHand::get_best([Joker, A, Joker, A, K]),
            Some(PokerHand::FourK)
        );
        assert_eq!(
            PokerHand::get_best([Joker, A, Joker, Q, K]),
            Some(PokerHand::ThreeK)
        );
        assert_eq!(
            PokerHand::get_best([Joker, A, T, Q, K]),
            Some(PokerHand::OneP)
        );
        assert_eq!(PokerHand::get_best([N2, A, T, Q, K]), Some(PokerHand::High));
        assert_eq!(PokerHand::TwoP, PokerHand::TwoP);
        
        assert_eq!(PokerHand::get_best([N8, Q, Q, Joker, N8]), Some(PokerHand::FullH));
    }
    #[test]
    fn cmp_hands() {
        let hand1 = Hand::new("32T3K 765");
        let hand2 = Hand::new("KK677 28");
        let hand3 = Hand::new("KTJJT 220");
        assert_eq!(hand1.cmp(&hand2), Ordering::Less);
        assert_eq!(hand2.cmp(&hand1), Ordering::Greater);
        assert_eq!(hand2.cmp(&hand3), Ordering::Greater);
    }
    #[test]
    fn cmp_joker() {
        let hand1 = Hand::new_with_joker("8QQJ8 10");
        let hand2 = Hand::new_with_joker("88J88 10");
        assert_eq!(hand1.cmp(&hand2), Ordering::Less);
        
    }
}
