import re
prod = True

inp = """\
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""
with open('input') as f:
    if prod: 
        inp = f.read()

mulreg = re.compile(r"mul\((\d{1,3}),(\d{1,3})\)")
smartreg = re.compile(r"mul\(\d{1,3},\d{1,3}\)|do\(\)|don't\(\)")
print(occ := mulreg.findall(inp))
print(sum([int(a)*int(b) for (a,b) in occ]))
print(occ2 := smartreg.findall(inp))
do = True
s = 0
for match in occ2:
    if match == "don't()":
        do = False
        continue
    if match == "do()":
        do = True
        continue
    a, b = re.match(r"mul\((\d*),(\d*)\)", match).groups()
    if do:
        s += int(a) * int(b)
print(s)

    
