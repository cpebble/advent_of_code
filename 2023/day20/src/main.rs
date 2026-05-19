use utils;
use std::{collections::HashMap, rc::Rc};
use std::hash::{DefaultHasher, Hash, Hasher};

enum ModuleType {
    FlipFlop,
    Conjunct,
    Broadcast,
}

enum ModuleState {
    FlipFlop(bool),
    Conjunct(Vec<bool>),
    Broadcast,
}
impl ModuleState {
    pub fn new(t: ModuleType) -> ModuleState {
        match t {
            ModuleType::FlipFlop => ModuleState::FlipFlop(false),
            ModuleType::Conjunct => ModuleState::Conjunct(Vec::new()),
            ModuleType::Broadcast => ModuleState::Broadcast,
        }
    }
}

struct Module {
    mid: u64,
    mtyp: ModuleType,
}

struct SystemState {
    modules: Vec<Rc<Module>>,
    mstates: HashMap<u64, ModuleState>,
    edges: Vec<(u64, u64)>
}
impl From<Vec<Module>> for SystemState {
    fn from(value: Vec<Module>) -> Self {
        let mut modules = Vec::new();
        let mut mstates = HashMap::new();
        let mut edges = Vec::new();
        for m in value {
            let mst = ModuleState::new(m.mtyp);

        }
    }
}

fn name_to_id(nm: &str) -> u64 {
    let mut s = DefaultHasher::new();
    nm.hash(&mut s);
    s.finish()
}

fn main() {
    let inp = utils::load_input(true, "day20");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> usize{
    return 0;
}
fn p2(inp: &str) -> usize{
    return 0;
}

#[cfg(test)]
mod tests {
    use crate::*;
    pub fn basic_module_system() -> SystemState {
        let broadcaster = Module {
            mid: name_to_id("broadcaster"),
            mtyp: ModuleType::Broadcast,
            children: Vec::new(),
        };
        let a = Module {
            mid: name_to_id("a"),
            mtyp: ModuleType::FlipFlop,
            children: Vec::new()
        }
        let b = Module {
            mid: name_to_id("b"),
            mtyp: ModuleType::FlipFlop,
            children: Vec::new()
        }
        let c = Module {
            mid: name_to_id("c"),
            mtyp: ModuleType::FlipFlop,
            children: Vec::new()
        }
        let inv = Module {
            mid: name_to_id("inv"),
            mtyp: ModuleType::Conjunct,
            children: Vec::new()
        }
    }

}
