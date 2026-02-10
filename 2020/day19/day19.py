
from collections import defaultdict
import sys
# sys.setrecursionlimit(99999)

TEST = True
test = """\
0: 4 1 5
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
1: 2 3 | 3 2
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb\
"""
test = """\
0: 8 11
1: "a"
2: 1 24 | 14 4
3: 5 14 | 16 1
4: 1 1
5: 1 14 | 15 1
6: 14 14 | 1 14
7: 14 5 | 1 21
8: 42
9: 14 27 | 1 26
10: 23 14 | 28 1
11: 42 31
12: 24 14 | 19 1
13: 14 3 | 1 12
14: "b"
15: 1 | 14
16: 15 1 | 14 14
17: 14 2 | 1 7
18: 15 15
19: 14 1 | 14 14
20: 14 14 | 1 15
21: 14 1 | 1 14
22: 14 14
23: 25 1 | 22 14
24: 14 1
25: 1 1 | 1 14
26: 14 22 | 1 20
27: 1 6 | 14 18
28: 16 1
31: 14 17 | 1 13
42: 9 14 | 10 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba"""
with open("day19.input") as f:
    realin = f.read()


inp = realin if TEST else test

(rules_s, msgs) = inp.split("\n\n")
# Parse Rules
rules = [None]*138
for rule_line in rules_s.splitlines():
    i, r = rule_line.split(":")
    rules[int(i)] = r.strip()

def parseList(text, rule_ids: list[int]) -> tuple[bool, list[str]]:
    if len(rule_ids) == 0:
        return (True, [text])
    v, leftovers = parse(text, rule_ids[0])
    if not v:
        return (False, leftovers)
    valids = []
    for leftover in leftovers:
        vsub, lsub = parseList(leftover, rule_ids[1:])
        if vsub:
            valids += lsub
    return (bool(valids), valids)

def parse(text: str, rule_id: int) -> tuple[bool, list[str]]:
    assert rules[rule_id] != None, f"Invalid rule {rule_id}"

    rule = rules[rule_id]
    # Handle split
    if "|" in rule:
        left_s, right_s = rule.split("|")
        left_i = list(map(int, left_s.strip().split(" ")))
        right_i = list(map(int, right_s.strip().split(" ")))
        v1, leftover1 = parseList(text, left_i)
        v2, leftover2 = parseList(text, right_i)
        if v1 and v2:
            #print(f"Split of '{leftover1}' and '{leftover2}'")
            return (True, leftover1 + leftover2)
        if v1:
            return (True, leftover1)
        if v2:
            return (True, leftover2)
        return (False, [f"Bad split in {rule_id} on text {text}"] + leftover1 + leftover2)
    # Handle Char
    elif rule[0] == '"':
        if len(text) != 0 and text[0] == rule[1]:
            return (True, [text[1:]])
        return (False, [])
    # Handle rule_list
    else:
        rule_ids = list(map(int, rule.split(" ")))
        return parseList(text, rule_ids)

def valid(text: str):
    valid, leftover = parse(text, 0)
    return valid and any(map(lambda x: x == "", leftover))

c = 0
for msg in msgs.splitlines():
    try:
        if valid(msg.strip()):
            c += 1
    except RecursionError:
        pass
        #print(msg)
print(c)

# Part 2
rules[8] = "42 | 42 8"
rules[11] = "42 31 | 42 11 31"

c = 0
for msg in msgs.splitlines():
    if valid(msg.strip()):
        c += 1
print(c)
