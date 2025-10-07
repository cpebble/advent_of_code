use regex::Regex;
use std::collections::VecDeque;
use std::iter::zip;

pub struct Evaluator {
    prog: Vec<isize>,
    ip: usize,
    pub halt: bool,
    pub waiting: bool,
    input: VecDeque<isize>,
    output: Vec<isize>,
    pub verbose: bool,
}
impl Evaluator {
    pub fn new(prog: &str) -> Evaluator {
        let re = Regex::new(r"-?\d\d*").unwrap();
        let intarr = re
            .find_iter(prog)
            .map(|m| m.as_str().parse::<isize>().expect("Regex fail"))
            .collect::<Vec<isize>>();
        Evaluator::from_vec(&intarr)
    }
    pub fn from_vec(arr: &[isize]) -> Evaluator {
        Evaluator {
            prog: arr.to_owned(),
            ip: 0,
            halt: false,
            waiting: false,
            output: Vec::new(),
            input: VecDeque::new(),
            verbose: false,
        }
    }
    fn step(&mut self) {
        if self.verbose {
            println!()
        };
        if self.halt {
            return;
        }
        // Fetch op
        let op = OpCode::new(self.prog[self.ip]);
        // Parse args
        let mut args = Vec::<usize>::new();
        for (i, pm) in zip(0..op.n_args, op.param_nodes) {
            let val = if pm == 0 {
                (self.prog[self.ip + 1 + i]).try_into().unwrap()
            } else {
                self.ip + 1 + i
            };
            args.push(val);
        }

        if self.verbose {
            print!(
                "[{:02}]{:04} {}: Args: {:?}",
                self.ip,
                self.prog[self.ip],
                as_str(op.num),
                args
            )
        };

        // RunOp
        let mut jmp = self.ip + 1 + op.n_args;
        match op.num {
            1 => {
                let v1 = self.prog[args[0]];
                let v2 = self.prog[args[1]];
                self.prog[args[2]] = v1 + v2;
                if self.verbose {
                    print!(" {} + {} = {}", v1, v2, v1 + v2)
                };
            }
            2 => {
                let v1 = self.prog[args[0]];
                let v2 = self.prog[args[1]];
                self.prog[args[2]] = v1 * v2;
                if self.verbose {
                    print!(" {} * {} = {}", v1, v2, v1 * v2)
                };
            }
            3 => match self.read() {
                Some(v) => {
                    self.prog[args[0]] = v;
                    if self.verbose {
                        print!("=: {}", self.prog[args[0]])
                    }
                }
                None => {
                    self.halt = true;
                    self.waiting = true;
                    jmp = self.ip;
                }
            },
            4 => {
                let v1 = self.prog[args[0]];
                if self.verbose {
                    print!("=: {}", v1)
                };
                self.write(v1);
            }
            5 => {
                let v1 = self.prog[args[0]];
                if v1 != 0 {
                    jmp = self.prog[args[1]] as usize;
                }
            }
            6 => {
                let v1 = self.prog[args[0]];
                if v1 == 0 {
                    jmp = self.prog[args[1]] as usize;
                }
            }
            7 => {
                let v1 = self.prog[args[0]];
                let v2 = self.prog[args[1]];
                let res = if v1 < v2 { 1 } else { 0 };
                self.prog[args[2]] = res
            }
            8 => {
                let v1 = self.prog[args[0]];
                let v2 = self.prog[args[1]];
                let res = if v1 == v2 { 1 } else { 0 };
                self.prog[args[2]] = res
            }

            99 => {
                self.halt = true;
                jmp = self.ip
            }
            _ => panic!("Unknown opcode {}", op.num),
        }
        self.ip = jmp;
    }

    pub fn run(self) -> Self {
        let mut ev = self;
        ev.halt = false;
        ev.waiting = false;
        while !ev.halt {
            ev.step();
        }
        ev
    }
    pub fn eval(&mut self) {
        self.halt = false;
        self.waiting = false;
        while !self.halt {
            self.step();
        }
    }

    pub fn load_input(&mut self, inp: isize) {
        self.input.push_back(inp);
    }
    pub fn get_output(&self) -> Vec<isize> {
        self.output.clone()
    }
    fn read(&mut self) -> Option<isize> {
        self.input.pop_front()
    }
    fn write(&mut self, val: isize) {
        self.output.push(val);
    }
}

pub struct OpCode {
    num: usize,
    n_args: usize,
    param_nodes: Vec<isize>,
}
impl OpCode {
    pub fn new(opcode: isize) -> OpCode {
        let op = opcode % 100;
        if op < 0 {
            panic!("Arithm err")
        }
        let (n_args, param_nodes) = match op {
            1 => (3, Self::three_args(opcode)), // Plus
            2 => (3, Self::three_args(opcode)), // Mul
            3 => (1, Self::one_arg(opcode)),    // Read
            4 => (1, Self::one_arg(opcode)),    // Write
            5 => (2, Self::two_args(opcode)),
            6 => (2, Self::two_args(opcode)),
            7 => (3, Self::three_args(opcode)),
            8 => (3, Self::three_args(opcode)),
            99 => (0, Vec::new()),
            _ => panic!("Unexpected op {}", op),
        };
        OpCode {
            num: op.try_into().expect("Arithm err in op"),
            n_args,
            param_nodes,
        }
    }
    fn three_args(opcode: isize) -> Vec<isize> {
        vec![
            (opcode / 100) % 10,
            (opcode / 1000) % 10,
            (opcode / 10000) % 10,
        ]
    }
    fn two_args(opcode: isize) -> Vec<isize> {
        vec![(opcode / 100) % 10, (opcode / 1000) % 10]
    }
    fn one_arg(opcode: isize) -> Vec<isize> {
        vec![(opcode / 100) % 10]
    }
}
fn as_str(op: usize) -> String {
    (match op {
        1 => "Plus",
        2 => "Mul",
        3 => "Read",
        4 => "Write",
        5 => "JIT",
        6 => "JIF",
        7 => "LT",
        8 => "EQ",
        99 => "Halt",
        x => panic!("Unexpected op {}", x),
    })
    .into()
}

pub fn parse_prog(prog: &str) -> Vec<isize> {
    let re = Regex::new(r"-?\d\d*").unwrap();
    re.find_iter(prog)
        .map(|m| m.as_str().parse::<isize>().expect("Regex fail"))
        .collect::<Vec<isize>>()
}

#[cfg(test)]
mod tests {
    use crate::*;
    static SIMPLEADDMULTEST: &str = "1,9,10,3,2,3,11,0,99,30,40,50";

    #[test]
    fn can_parse() {
        Evaluator::new(SIMPLEADDMULTEST);
    }

    #[test]
    fn simpleaddmul() {
        let mut ev = Evaluator::new(SIMPLEADDMULTEST);
        ev.step();
        ev.step();
        assert!(!ev.halt);
        ev.step();
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
            let mut ev = Evaluator::from_vec(&start);
            println!("{:?}->{:?}", start, end);
            ev = ev.run();
            assert_eq!(ev.prog, end);
        }
    }
    #[test]
    fn posmodes() {
        let sprogs = [(vec![1002, 4, 3, 4, 33], vec![1002, 4, 3, 4, 99])];
        for (start, end) in sprogs {
            let mut ev = Evaluator::from_vec(&start);
            ev = ev.run();
            assert_eq!(ev.prog, end);
        }
    }

    #[test]
    fn ioprogs() {
        let sprogs = [
            (vec![3, 0, 4, 0, 99], vec![5]),
            (vec![3, 0, 102, 3, 0, 0, 4, 0, 99], vec![15]),
            (vec![3, 0, 4, 0, 102, 3, 0, 0, 4, 0, 99], vec![5, 15]),
        ];
        for (start, output) in sprogs {
            let mut ev = Evaluator::from_vec(&start);
            ev.load_input(5);
            println!("{:?}->{:?}", start, output);
            ev = ev.run();
            assert_eq!(ev.output, output);
        }
    }
    #[test]
    fn iohalt() {
        let prog = parse_prog("3,0,4,0,99");
        let mut ev = Evaluator::from_vec(&prog);
        ev.eval();
        assert!(ev.halt);
        assert!(ev.waiting);
        ev.load_input(5);
        ev.eval();
        assert!(ev.halt);
        assert!(!ev.waiting);
        assert_eq!(ev.output.last(), Some(&5));
    }
}
