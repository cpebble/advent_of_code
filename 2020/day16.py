import re

inp = open("day16.input").read().split("\n\n")
_inp = """\
class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9
""".split("\n\n")

def testRule(n, rule):
    return (rule["al"] <= n <= rule["ah"]) or \
           (rule["bl"] <= n <= rule["bh"])

nFields = len(inp[2].strip().split("\n")[-1].split(","))

rules = {}
# Read rules in first
ruleRegex = r"(.+): (\d+)-(\d+) or (\d+)-(\d+)"
for r in inp[0].split("\n"):
    fname, al, ah, bl, bh = re.match(ruleRegex, r).groups()
    print(f"fname: {fname}, second high: {bh}")
    rules[fname] = {
            "name": fname,
            "al": int(al),
            "ah": int(ah),
            "bl": int(bl),
            "bh": int(bh),
            "possible": set(range(nFields))
            }

print(rules)

scanerror = 0
for ticket in inp[2].strip().split("\n")[1:]:
    for field in ticket.strip().split(","):
        try:
            n = int(field)
        except:
            breakpoint()
        # Test all rules
        if not any(map(lambda r: testRule(n, r), rules.values())):
            #print(f"{n} matches no rule")
            scanerror += n
print(scanerror)

isAllValid = lambda n: any(map(lambda r: testRule(n, r), rules.values()))
# Get valid tickets
valid_tickets = [list(map(int, t.split(","))) \
        for t in inp[2].strip().split("\n")[1:] \
        if all(map(lambda n: isAllValid(int(n)), t.split(",")))
            ]
#print(valid_tickets)

# Now figure out possible positions
for rulename, rule in rules.items():
    possible = set()
    for i in range(nFields):
        if all(map(lambda n: testRule(n[i], rule), valid_tickets)):
            possible.add(i)
    rule["possible"] = possible
#print(rules)

# Finally narrow these down:
found = set()
ls = sorted(rules.items(), key=lambda r: len(r[1]["possible"]))
print("###")
for name, rule in ls:
    fields = rule["possible"] - found
    if len(fields) == 1:
        # This is the only valid field for this rule
        found |= fields
        rule["index"] = fields.pop()

# The above two loops can be put together, but sorting by
# len(possible) allows me to always make the greedy choice

for n, r in rules.items():
    print(f"[{n}]: {r['index']}")

# Finally calculate ticket
s = 1
for na, r in rules.items():
    if na.startswith("departure"):
        n = int(inp[1].strip().split("\n")[1].strip().split(",")[r["index"]])
        s *= n
        print(f"{na}: {n}")
print(s)
