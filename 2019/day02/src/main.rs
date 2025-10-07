use regex::Regex;
use utils;

static TEST: &str = "1,9,10,3,2,3,11,0,99,30,40,50";

struct Evaluator {
    prog: Vec<usize>,
    ip: usize,
    halt: bool,
}
impl Evaluator {
    fn new(prog: &str) -> Evaluator {
        let re = Regex::new(r"\d\d*").unwrap();
        let intarr = re
            .find_iter(prog)
            .map(|m| m.as_str().parse::<usize>().expect("Regex fail"))
            .collect::<Vec<usize>>();

        Evaluator {
            prog: intarr,
            ip: 0,
            halt: false,
        }
    }
    fn from_vec(arr: &Vec<usize>) -> Evaluator {
        Evaluator {
            prog: arr.clone(),
            ip: 0,
            halt: false,
        }
    }
    fn step(mut self) -> Self {
        if self.halt {
            return self;
        }
        // Fetch op
        let op = self.prog[self.ip];
        // Parse args
        let nargs = num_args(op);
        let mut args = Vec::new();
        for i in 0..nargs {
            args.push(self.prog[self.ip + 1 + i]);
        }

        // RunOp
        match op {
            1 => {
                let v1 = self.prog[args[0]];
                let v2 = self.prog[args[1]];
                self.prog[args[2]] = v1 + v2;
                //println!("Add {} + {} to {}", v1, v2, args[2])
            }
            2 => {
                let v1 = self.prog[args[0]];
                let v2 = self.prog[args[1]];
                self.prog[args[2]] = v1 * v2;
                //println!("Mul {} * {} to {}", v1, v2, args[2])
            }
            99 => self.halt = true,
            _ => panic!("Unknown opcode {}", op),
        }
        self.ip += 1 + nargs;
        self
    }

    fn run(self) -> Self {
        let mut ev = self;
        while !ev.halt {
            ev = ev.step();
        }
        ev
    }
}
fn num_args(opcode: usize) -> usize {
    match opcode {
        1..=2 => 3,
        99 => 0,
        _ => panic!("Unknown opcode {}", opcode),
    }
}

fn main() {
    let inp = utils::load_input(true, "day02");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> usize {
    let mut eval = Evaluator::new(inp);
    eval.prog[1] = 12;
    eval.prog[2] = 2;
    eval = eval.run();
    eval.prog[0]
}
fn p2(inp: &str) -> usize {
    let initeval = Evaluator::new(inp);
    let prog = initeval.prog;
    for i in 0..=99 {
        for j in 0..=99 {
            let mut ev = Evaluator::from_vec(&prog);
            ev.prog[1] = i;
            ev.prog[2] = j;
            ev=ev.run();
            if ev.prog[0] == 19690720{
                return 100*i + j;
            }
        }
    }
    panic!();
}

#[cfg(test)]
mod tests {
    use crate::*;
    static TEST: &str = "1,9,10,3,2,3,11,0,99,30,40,50";

    #[test]
    fn can_parse() {
        Evaluator::new(TEST);
    }

    #[test]
    fn simpleaddmul() {
        let mut ev = Evaluator::new(TEST);
        ev = ev.step();
        ev = ev.step();
        assert!(!ev.halt);
        ev = ev.step();
        assert!(ev.halt);
        println!("{:?}", ev.prog);
        assert_eq!(ev.prog[3], 70);
        assert_eq!(ev.prog[0], 3500);
    }

    #[test]
    fn smallprogs() {
        let sprogs = [
            (vec![1, 0, 0, 0, 99], vec![2, 0, 0, 0, 99]),
            (vec![2, 3, 0, 3, 99], vec![2, 3, 0, 6, 99]),
            (vec![2, 4, 4, 5, 99, 0], vec![2, 4, 4, 5, 99, 9801]),
            (
                vec![1, 1, 1, 4, 99, 5, 6, 0, 99],
                vec![30, 1, 1, 4, 2, 5, 6, 0, 99],
            ),
        ];
        for (start, end) in sprogs {
            let mut ev = Evaluator::from_vec(start);
            ev = ev.run();
            assert_eq!(ev.prog, end);
        }
    }
}
