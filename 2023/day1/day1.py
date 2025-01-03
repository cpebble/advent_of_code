import sys
import re

pat1 = r"([1-9])"
pat2 = r"([1-9]|one|two|three|four|five|six|seven|eight|nine)"

def parseword(s):
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" ]
    if s in words:
        return words.index(s)
    return int(s)

x = sys.argv[1]
with open(x) as f:
    inp = f.read().rstrip()

p1 = 0
p2 = 0
for l in inp.split("\n"):
    gs1 = re.findall(pat1, l)
    gs2 = re.findall(pat2, l)
    print(gs2[0], gs2[-1])
    try:
        p1 += parseword(gs1[0])*10 + parseword(gs1[-1])
    except:
        pass
    try:
        p2 += parseword(gs2[0])*10 + parseword(gs2[-1])
    except:
        print("!", l)

print(p1, p2)
