use regex::Regex;
use std::{
    collections::{HashMap, VecDeque},
    str::Chars,
};
use utils;

fn main() {
    let inp = utils::load_input(true, "day19");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}

#[derive(Debug)]
enum Action {
    Goto(Box<str>),
    Accept,
    Reject,
}
impl From<char> for Action {
    fn from(value: char) -> Self {
        match value {
            'R' => Action::Reject,
            'A' => Action::Accept,
            _ => panic!("Cannot match {value} as action"),
        }
    }
}
impl From<String> for Action {
    fn from(value: String) -> Self {
        if value == "R" {
            Action::Reject
        } else if value == "A" {
            Action::Accept
        } else {
            let v_ = value.clone();
            let b = Box::from(v_);
            Action::Goto(b)
        }
    }
}

#[derive(Debug)]
enum Cond {
    Any,
    LT { vn: char, target: usize },
    GT { vn: char, target: usize },
}
impl Cond {
    fn eval(&self, part: &Part) -> bool {
        match self {
            Self::Any => true,
            Self::LT { vn, target } => part.get(*vn) < *target,
            Self::GT { vn, target } => part.get(*vn) > *target,
        }
    }
}

#[derive(Debug)]
struct Rule {
    cond: Cond,
    action: Action,
}
#[derive(Debug)]
struct Workflow {
    name: Box<str>,
    rules: Vec<Rule>,
}

#[derive(Debug, Copy, Clone)]
struct Part {
    x: usize,
    m: usize,
    a: usize,
    s: usize,
}
impl Part {
    fn get(&self, c: char) -> usize {
        match c {
            'x' => self.x,
            'm' => self.m,
            'a' => self.a,
            's' => self.s,
            _ => panic!("{c} ain't no part i've ever seen"),
        }
    }
    fn val(&self) -> usize {
        self.x + self.m + self.a + self.s
    }
}
impl From<&str> for Part {
    fn from(value: &str) -> Self {
        let part_regex =
            Regex::new(r"\{x=(?<x>\d+),m=(?<m>\d+),a=(?<a>\d+),s=(?<s>\d+)\}").unwrap();
        // {x=787,m=2655,a=1222,s=2876}
        let caps = part_regex.captures(value).unwrap();
        Part {
            x: caps["x"].parse::<usize>().unwrap(),
            m: caps["m"].parse::<usize>().unwrap(),
            a: caps["a"].parse::<usize>().unwrap(),
            s: caps["s"].parse::<usize>().unwrap(),
        }
    }
}

fn parseWorkFlow(line: &str) -> Workflow {
    let mut line_reader = line.chars();

    // Parse name
    let nm: String = until(&mut line_reader, '{');

    // Start parsing workflow
    let mut rules: Vec<Rule> = Vec::new();

    loop {
        // Read attr
        let attr = get_c(&mut line_reader);
        // GT or LT
        let gt = get_c(&mut line_reader);
        if gt == '}' {
            // We reached the end and it's not a jump
            rules.push(Rule {
                cond: Cond::Any,
                action: Action::from(attr),
            });
            break;
        }
        if gt != '>' && gt != '<' {
            // We reached the end and it's a jump
            let gotostr = until(&mut line_reader, '}');
            let mut final_str = String::new();
            final_str.push(attr);
            final_str.push(gt);
            final_str.push_str(&gotostr);
            rules.push(Rule {
                cond: Cond::Any,
                action: Action::from(final_str),
            });
            break;
        }
        // Otherwise, read an integer
        let num = until(&mut line_reader, ':').parse::<usize>().unwrap();
        // Read an action
        let action = until(&mut line_reader, ',');

        // Assemble the rule
        let cond_t = if gt == '>' {
            Cond::GT {
                vn: attr,
                target: num,
            }
        } else {
            Cond::LT {
                vn: attr,
                target: num,
            }
        };
        // Add to list of rules
        let rule = Rule {
            cond: cond_t,
            action: Action::from(action),
        };
        rules.push(rule);
    }
    Workflow {
        name: Box::from(nm),
        rules: rules,
    }
}

fn run_workflow(part: &Part, wfs: &HashMap<&str, &Workflow>) -> bool {
    let mut target = "in";
    loop {
        let current = *wfs.get(&target).expect("Couldn't find target {target}");
        for rule in &(current.rules) {
            if !rule.cond.eval(part) {
                continue;
            }
            match &rule.action {
                Action::Goto(new_label) => {
                    target = &new_label;
                    break;
                }
                Action::Accept => return true,
                Action::Reject => return false,
            }
        }
    }
}

/// Get a single char from stream
fn get_c(cs: &mut Chars) -> char {
    match cs.next() {
        Some(c) => c,
        None => panic!("Unexpected EOF"),
    }
}
/// get a string until a char is found
/// consumes the tailing char
fn until(cs: &mut Chars, t: char) -> String {
    let mut outstr = String::new();
    loop {
        let c = cs
            .next()
            .expect("Unexpected EOF waiting for '{t}', Got \"{outstr}\"");
        if c == t {
            return outstr;
        } else {
            outstr.push(c)
        }
    }
}
/// get a string until one of a list of chars is found
/// consumes the tailing char
fn untils(cs: &mut Chars, t: &[char]) -> String {
    let mut outstr = String::new();
    loop {
        let c = cs
            .next()
            .expect("Unexpected EOF waiting for '{t}', Got \"{outstr}\"");
        if t.contains(&c) {
            return outstr;
        } else {
            outstr.push(c)
        }
    }
}

fn p1(inp: &str) -> usize {
    let mut inps = inp.split("\n\n");
    let wfs_unparsed = inps.next().unwrap();
    let wfs: Vec<Workflow> = wfs_unparsed.lines().map(parseWorkFlow).collect();
    let wf_map: HashMap<&str, &Workflow> = wfs.iter().map(|wf| (&(*(wf.name)), wf)).collect();

    let parts: Vec<Part> = inps.next().unwrap().lines().map(Part::from).collect();

    let mut ret = 0;
    for p in parts {
        //print!("Part x: {} - ", p.x);
        let valid = run_workflow(&p, &wf_map);
        if valid {
            ret += p.val()
        }
        //println!("{valid}");
    }
    return ret;
}

#[derive(Debug, Clone, Copy)]
struct Range {
    lower: usize,
    upper: usize,
}
impl Range {
    fn split_lt(self, new_val: usize) -> (Range, Range) {
        let lower = Range {
            lower: self.lower,
            upper: new_val - 1,
        };
        let upper = Range {
            lower: new_val,
            upper: self.upper,
        };
        return (lower, upper);
    }
    fn split_gt(self, new_val: usize) -> (Range, Range) {
        let lower = Range {
            lower: self.lower,
            upper: new_val,
        };
        let upper = Range {
            lower: new_val + 1,
            upper: self.upper,
        };
        return (upper, lower);
    }
}

#[derive(Debug, Clone, Copy)]
struct PartRange {
    x: Range,
    m: Range,
    a: Range,
    s: Range,
}

impl PartRange {
    fn fmt(&self) -> String {
        format!(
            "x = {}-{}; m = {}-{}; a = {}-{}; s = {}-{}",
            self.x.lower,
            self.x.upper,
            self.m.lower,
            self.m.upper,
            self.a.lower,
            self.a.upper,
            self.s.lower,
            self.s.upper
        )
    }

    fn get(&self, c: char) -> Range {
        match c {
            'x' => self.x,
            'm' => self.m,
            'a' => self.a,
            's' => self.s,
            _ => panic!("{c} ain't no part i've ever seen"),
        }
    }
    fn set(&mut self, c: char, r: Range) {
        match c {
            'x' => self.x = r,
            'm' => self.m = r,
            'a' => self.a = r,
            's' => self.s = r,
            _ => panic!("{c} ain't no part i've ever seen"),
        };
    }

    fn val(&self) -> usize {
        ((self.x.upper - self.x.lower) + 1 )* 
        ((self.m.upper - self.m.lower) + 1 )* 
        ((self.a.upper - self.a.lower) + 1 )* 
        ((self.s.upper - self.s.lower) + 1 )
    }

    fn split(&self, cond: &Cond) -> (Option<PartRange>, Option<PartRange>) {
        // Return: Left is successes, Right is Fails
        match cond {
            Cond::Any => (Some(self.clone()), None),
            Cond::LT { vn, target } => {
                let range = self.get(*vn);
                if range.upper < *target {
                    return (Some(self.clone()), None);
                }
                if range.lower > *target {
                    return (None, Some(self.clone()));
                }
                let (passing, failing) = range.split_lt(*target);
                let mut passing_parts = self.clone();
                passing_parts.set(*vn, passing);
                let mut failing_parts = self.clone();
                failing_parts.set(*vn, failing);
                return (Some(passing_parts), Some(failing_parts));
            }
            Cond::GT { vn, target } => {
                let range = self.get(*vn);
                if range.lower > *target {
                    return (Some(self.clone()), None);
                }
                if range.upper < *target {
                    return (None, Some(self.clone()));
                }
                let (passing, failing) = range.split_gt(*target);

                let mut passing_parts = self.clone();
                passing_parts.set(*vn, passing);

                let mut failing_parts = self.clone();
                failing_parts.set(*vn, failing);
                return (Some(passing_parts), Some(failing_parts));
            }
        }
    }
}

fn p2(inp: &str) -> usize {
    let mut inps = inp.split("\n\n");
    let wfs_unparsed = inps.next().unwrap();
    let wfs: Vec<Workflow> = wfs_unparsed.lines().map(parseWorkFlow).collect();
    let wf_map: HashMap<&str, &Workflow> = wfs.iter().map(|wf| (&(*(wf.name)), wf)).collect();

    // Starting with In
    let full_range = PartRange {
        x: Range {
            lower: 1,
            upper: 4000,
        },
        m: Range {
            lower: 1,
            upper: 4000,
        },
        a: Range {
            lower: 1,
            upper: 4000,
        },
        s: Range {
            lower: 1,
            upper: 4000,
        },
    };
    println!("Full: {}", full_range.fmt());

    let mut workset: VecDeque<(&Workflow, PartRange)> = VecDeque::new();
    let mut passing_parts: Vec<PartRange> = Vec::new();

    workset.push_back((&wf_map.get("in").unwrap(), full_range));

    while workset.len() > 0 {
        let (wf, part_) = workset.pop_front().unwrap();
        let mut part = part_.to_owned();
        for rule in &wf.rules {
            let (passing, failing) = part.split(&rule.cond);
            match passing {
                None => (),
                // Perform action, then stop evaluating rules
                Some(parts) => match &rule.action {
                    Action::Goto(lab) => {
                        let new_wf = wf_map.get(&(**lab)).unwrap();
                        workset.push_back((new_wf, parts.clone()))
                    }
                    Action::Accept => {
                        passing_parts.push(parts.clone());
                    }
                    Action::Reject => (),
                }
            };
            match failing {
                None => break,
                Some(new_part) => part = new_part,
            }
        }
    }
    let mut sum = 0;
    for p in &passing_parts {
        sum += p.val();
    }

    return sum;
}
