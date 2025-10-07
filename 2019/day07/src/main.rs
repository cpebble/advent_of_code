use intcode::{Evaluator, parse_prog};
use itertools::Itertools;
use utils;

fn main() {
    let inp = utils::load_input(true, "day07");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}

struct Amplifier {
    id: isize,
    evaluator: Evaluator,
}
impl Amplifier {
    fn new(ident: isize, prog: &str, phase: isize) -> Amplifier {
        let mut ev = Evaluator::new(prog);
        ev.load_input(phase);
        Amplifier {
            id: ident,
            evaluator: ev,
        }
    }
    fn new_(ident: isize, prog: &[isize], phase: isize) -> Amplifier {
        let mut ev = Evaluator::from_vec(prog);
        ev.load_input(phase);
        Amplifier {
            id: ident,
            evaluator: ev,
        }
    }
}
fn p1(inp: &str) -> isize {
    let prog = parse_prog(inp);

    let mut maxs = 0;
    let mut maxval = 0;
    for seq in (0..5).permutations(5) {
        let [a, b, c, d, e] = seq.try_into().unwrap();
        let val = a * 10000 + b * 1000 + c * 100 + d * 10 + e;
        let res = run_phasesetting_(&prog, val);
        if res > maxval {
            maxs = val;
            maxval = res;
        }
    }
    return maxval;
}

fn run_phasesetting(inp: &str, phase: isize) -> isize {
    let prog = parse_prog(inp);
    run_phasesetting_(&prog, phase)
}
fn run_phasesetting_(inp: &[isize], phase: isize) -> isize {
    let mut evs = Vec::new();
    let mut phase_ = phase;
    let mut i = 0;
    while phase_ > 0 {
        let x = phase_ % 10;
        let ev = Amplifier::new_(i, inp, x);
        evs.push(ev);
        i += 1;
        phase_ /= 10;
    }
    while i < 5 {
        evs.push(Amplifier::new_(i, inp, 0));
        i += 1;
    }
    let mut signal = 0;
    evs.reverse();
    for amp in evs {
        let mut ev = amp.evaluator;
        ev.load_input(signal);
        signal = *ev.run().get_output().last().unwrap();
        // let signal = ev.get_output().first();
    }

    return signal;
}
fn run_phasesetting2(inp: &[isize], phase: isize) -> isize {
    //let mut evs = Vec::new();
    let mut phase_ = phase;
    let mut evs = [
        Evaluator::from_vec(inp),
        Evaluator::from_vec(inp),
        Evaluator::from_vec(inp),
        Evaluator::from_vec(inp),
        Evaluator::from_vec(inp)
    ];
    let mut i = 0;
    while phase_ > 0 {
        let x = phase_ % 10;
        evs[i].load_input(x);
        i += 1;
        phase_ /= 10;
    }
    while i < 5 {
        evs[i].load_input(0);
        i += 1;
    }
    evs.reverse();
    // Now we start looping
    let mut signal = 0;
    let mut done = false;
    while !done {
        for i in 0..5 {
            evs[i].load_input(signal);
            evs[i].eval();
            signal = *evs[i].get_output().last().unwrap();
            //println!(
                //"Amp {} H {} W {}",
                //i, evs[i].halt, ev.waiting
            //);
        }
        if !evs[0].waiting {
            done = true;
        }
    }

    return signal;
}

fn p2(inp: &str) -> isize {
    let prog = parse_prog(inp);

    let mut maxs = 0;
    let mut maxval = 0;
    for seq in (5..=9).permutations(5) {
        let [a, b, c, d, e] = seq.try_into().unwrap();
        let val = a * 10000 + b * 1000 + c * 100 + d * 10 + e;
        let res = run_phasesetting2(&prog, val);
        //println!("{} : {}", res, val);
        if res > maxval {
            maxs = val;
            maxval = res;
        }
    }
    return maxval;
}

mod tests {
    use crate::*;
    static TEST: &str = "";

    #[test]
    fn testrun() {
        let inp = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0";
        let phase = 43210;
        assert_eq!(run_phasesetting(inp, phase), 43210)
    }
    #[test]
    fn testex2() {
        let inp = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0";
        let phase = 1234;
        assert_eq!(run_phasesetting(inp, phase), 54321);
    }
    #[test]
    fn testex3() {
        let inp = "3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0";
        let phase = 10432;
        assert_eq!(run_phasesetting(inp, phase), 65210);
    }
    #[test]
    fn testrun2() {
        let inp = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0";
        let phase = 44444;
        let mut ev = Evaluator::new(inp);
        ev.load_input(4);
        ev.load_input(0);
        let mut ev2 = Evaluator::new(inp);
        ev2.load_input(4);
        ev2.load_input(4);
        ev2.verbose = true;
        println!("{:?}", ev2.run().get_output());
        assert_eq!(run_phasesetting(inp, phase), 44444)
    }
    #[test]
    fn p1example() {
        let inp = "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0";
        let target = 43210;
        assert_eq!(p1(inp), target);
    }
    #[test]
    fn p2example() {
        let inp =
            "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5";
        let target = 139629729;
        assert_eq!(p2(inp), target);
    }
}
