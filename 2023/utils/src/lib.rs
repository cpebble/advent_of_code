use std::fs::File;
use std::io::Read;
use std::path::Path;

//static PROD: bool = false;
//static DAY: &str = "day1";
pub fn load_input(prod: bool, day: &str) -> String {
    let path: String = match prod {
        true => format!("inputs/{}.input", day),
        false => format!("inputs/{}.example", day),
    };
    let mut file = match File::open(Path::new(&path)) {
        Ok(s) => s,
        Err(why) => panic!("AAAAAAAAAAA {}\n", why),
    };
    let mut out = String::new();
    match file.read_to_string(&mut out) {
        Ok(_) => (),
        Err(why) => panic!("BBBBBBBBB {}\n", why),
    }
    return out;
}

#[cfg(test)]
mod tests {

    #[test]
    fn it_works() {
        assert_eq!(4, 4);
    }
}
