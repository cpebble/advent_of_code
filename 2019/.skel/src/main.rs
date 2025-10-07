use utils;

fn main() {
    let inp = utils::load_input(true, "{{DAY}}");
    println!("Part 1: {}", p1(&inp));
    println!("Part 2: {}", p2(&inp));
}
fn p1(inp: &str) -> i32{
    return 0;
}
fn p2(inp: &str) -> i32{
    return 0;
}


mod tests {
    use crate::*;
    static TEST: &str = "";

    #[test]
    fn p1example() {
        let inp = TEST;
        let target = 0;
        assert_eq!(p1(inp), target);
    }
    #[test]
    fn p2example() {
        let inp = TEST;
        let target = 0;
        assert_eq!(p2(inp), target);
    }
}
