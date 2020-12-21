from re import search

inp = open("day14.input").readlines()
_inp = """\
mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1\
""".split("\n")

def readmask(mask):
    i = 0
    high = 0
    low = 0
    while(i < len(mask)):
        if mask[-i-1] == "1":
            high = high | (1<<i)
        elif mask[-i-1] == "0":
            low = low | (1<<i)
        i+=1
    low = low ^ 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFfF
    return high, low


def allmasks(mask):
    """Stolened from /u/jonathan_paulson"""
    if not mask:
        yield ''
        return
    for m in allmasks(mask[1:]):
        if mask[0] == '0':
            yield 'X' + m  # leave unchanged
        elif mask[0] == '1':
            yield '1' + m  # replace with 1
        elif mask[0] == 'X':
            yield '0' + m  # replace with 0
            yield '1' + m  # replace with 1

def maskno(high, low, no):
    n2 = no | high
    n = n2 & low
    return n


mem = {}
for line in inp:
    line = line.strip()
    if line.startswith("mask"):
        high, low = readmask(line.split(" ")[2])
        continue
    addr = int(search(r"mem\[(\d+)\]", line).group(1))
    num = int(line.split(" ")[2])
    mem[addr] = maskno(high, low, num)
print(sum(mem.values()))

# Part 2
mem = {}
for line in inp:
    line = line.strip()
    if line.startswith("mask"):
        mask = line.split(" = ")[1]
        continue
    addr = int(search(r"mem\[(\d+)\]", line).group(1))
    num = int(line.split(" ")[2])
    print("###",num)
    for m in allmasks(mask):
        h, l = readmask(m)
        print(maskno(h,l,addr))
        mem[maskno(h, l, addr)] = num

print(sum(mem.values()))

