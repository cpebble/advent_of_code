import re
def checkPassport(pas):
    try:
        a = (1920 <= int(pas["byr"]) <= 2002)
        b = (2010 <= int(pas["iyr"]) <= 2020)
        c = (2020 <= int(pas["eyr"]) <= 2030)
        d_ = re.match(r"(\d*)(in|cm)", pas["hgt"])
        d = False
        if d_ is not None:
            if d_[2] == "in":
                d = (59 <= int(d_[1]) <= 76)
            elif d_[2] == "cm":
                d = (150 <= int(d_[1]) <= 193)
        e = (re.match(r"#[0-9a-f]{6}$", pas["hcl"]) is not None)
        f = (re.match(r"^[0-9]{9}$", pas["pid"]) is not None)
        g = pas["ecl"] in ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
        print(a, b, c, d, e, f, g)
        return (a and b and c and d and e and f and g)
    except KeyError:
        return False




with open("day4.input") as f:
    lines = f.read().split("\n\n")

    counts = 0
    passport = {}
    reading = 0
    for line in lines:
        passport = {}
        line = line.replace("\n", " ")
        fields = line.split(" ")
        for e in fields:
            if e == "":
                continue
            x = e.split(":")
            passport[x[0]] = x[1].strip()
        #print(passport)
        if checkPassport(passport):
            print(line)
            counts+=1
    print(counts)
