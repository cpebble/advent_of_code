use utils;

fn main() {
    let inp = utils::load_input(true, "day9");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}

fn run(nums: Vec<isize>) -> isize {
    //println!("{:?}", utils::strvec(&nums, ","));
    if nums.iter().all(|n| *n == 0) {
        return 0;
    }
    let nextline: Vec<isize> = (1..(nums.len())).map(|i| (nums[i] - nums[i - 1])).collect();
    let val = run(nextline);
    return nums.last().unwrap() + val;
}

fn p1(inp: &str) -> isize {
    inp.lines()
        .map(|l| utils::parse_numbers(l))
        .map(|nums| run(nums))
        .sum()
}
fn p2(inp: &str) -> isize {
    inp.lines()
        .map(|l| utils::parse_numbers(l))
        .map(|mut nums| {nums.reverse(); nums})
        .map(|nums| run(nums))
        .sum()
}

#[cfg(test)]
mod tests {
    use crate::run;

    #[test]
    pub fn test1() {
        assert_eq!(run(vec!(0, 3, 6, 9, 12, 15)), 18);
        assert_eq!(run(vec!(0, 3, 6, 9, 12, 15)), 18);
        assert_eq!(run(vec!(1, 3, 6, 10, 15, 21)), 28);
        assert_eq!(run(vec!(10, 13, 16, 21, 30, 45)), 68);
    }
    #[test]
    pub fn test2() {
        assert_eq!(run(vec!(45,  30, 21, 16, 13, 10)), 5);
        //assert_eq!(run(vec!(15, 12, 9, 6, 3, 0)), 18);
        //assert_eq!(run(vec!(0, 3, 6, 9, 12, 15)), 18);
        //assert_eq!(run(vec!(1, 3, 6, 10, 15, 21)), 28);
    }
}
