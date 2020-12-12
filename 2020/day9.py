

lines = [int(x.strip()) for x in open("day9.input").readlines()]
preamble = 25
inp = lines[:preamble]
print(inp)
res = 0
for i in range(preamble, len(lines)):
    num = lines[i]
    found = False
    for j in range(i-preamble, i):
        for j_ in range(j, i):
            if lines[j] + lines[j_] == num:
                found = True
    if not found:
        res = lines[i]
        break
print(res)

for i in range(len(lines)):
    s = lines[i]
    j = i + 1
    while(s < res):
        s += lines[j]
        j += 1
    if s == res:
        print(lines[i:j+1])
        print(f"Sum: {sum(lines[i:j])}, min: {min(lines[i:j])}, max: {max(lines[i:j])}")
