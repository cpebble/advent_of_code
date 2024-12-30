from multiprocessing import Event, Pool
import re


prod = True
debug = False
inp = """\
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
""".rstrip()

with open("input") as f:
    if prod:
        inp = f.read()
        inp.rstrip()

regs_, prog = inp.split("\n\n")

prog = re.findall(r"\d+", prog)
regs_ = re.findall(r"\d+", regs_)
prog = list(map(int, prog))
regs = list(map(int, regs_))


def run(regs, prog):
    ip = 0
    output = []
    while ip < len(prog):

        # Read instruction
        ins = prog[ip]
        # Read parameter
        parm = prog[ip+1]
        if ins in [0, 2, 5, 6, 7]:
            if parm > 3:
                parm = regs[parm - 4]

        if debug: print(f"""\
    |--------------------
    |Register A: {regs[0]}
    |Register B: {regs[1]}
    |Register C: {regs[2]}
    |
    |Prog: {prog}
    |IP:    {" "*3*ip}^
    |Parm: {parm}
    |
    |Out: {output}
    """)

        if debug: input()
        # Default offset
        offset = 2
        
        # Run op
        if ins == 0:   # A := trunc(A // 2**combo)
            regs[0] = regs[0] // (2**parm)
        elif ins == 1: # B := B xor imm
            regs[1] = regs[1] ^ parm
        elif ins == 2: # B := combo % 8
            regs[1] = parm % 8
        elif ins == 3: # jnz A imm
            if regs[0] != 0:
                ip = parm
                offset = 0
        elif ins == 4: # B := B xor C
            regs[1] = regs[1] ^ regs[2]
        elif ins == 5: # out += combo % 8
            output.append(parm % 8)
        elif ins == 6: # B := trunc(A // 2**combo)
            regs[1] = regs[0] // (2**parm)
        elif ins == 7: # C := trunc(A // 2**combo)
            regs[2] = regs[0] // (2**parm)

        # Increase ip
        ip += offset
    return output
if not prod:
    assert run(regs, prog) == [4,6,3,5,6,3,5,2,1,0]
output = run(regs, prog)
print(",".join(map(str, output)))

# Part2

def runexpect(regs, prog):
    a = regs[0]
    i = 0
    ip = 0
    output = []
    while ip < len(prog):

        # Read instruction
        ins = prog[ip]
        # Read parameter
        parm = prog[ip+1]
        if ins in [0, 2, 5, 6, 7]:
            if parm > 3:
                parm = regs[parm - 4]

        if debug: print(f"""\
    |--------------------
    |Register A: {regs[0]}
    |Register B: {regs[1]}
    |Register C: {regs[2]}
    |
    |Prog: {prog}
    |IP:    {" "*3*ip}^
    |Parm: {parm}
    |
    |Out: {output}
    """)

        if debug: input()
        # Default offset
        offset = 2
        
        # Run op
        if ins == 0:   # A := trunc(A // 2**combo)
            regs[0] = regs[0] // (2**parm)
        elif ins == 1: # B := B xor imm
            regs[1] = regs[1] ^ parm
        elif ins == 2: # B := combo % 8
            regs[1] = parm % 8
        elif ins == 3: # jnz A imm
            if regs[0] != 0:
                ip = parm
                offset = 0
        elif ins == 4: # B := B xor C
            regs[1] = regs[1] ^ regs[2]
        elif ins == 5: # out += combo % 8
            out = parm % 8
            if out != prog[i]:
                return False
            i += 1
            #output.append(parm % 8)
        elif ins == 6: # B := trunc(A // 2**combo)
            regs[1] = regs[0] // (2**parm)
        elif ins == 7: # C := trunc(A // 2**combo)
            regs[2] = regs[0] // (2**parm)

        # Increase ip
        ip += offset
    return (i == len(prog))


def pr(a):
    print(list( map(lambda e: hex(e), a)))
def cmparr(a, b):
    if len(a) != len(b):
        return False
    for x, y in zip(a, b):
        if x != y:
            return False
    return True
code = []
for i in range(1, len(prog) + 1):
    target = prog[-i:]
    a = 0
    for x in code:
        a = a << 3
        a += x
    a = a << 3
    for j in range(0, 0xff):
        x = run([a + j, 0, 0], prog)
        if cmparr(x, target):
            if False: print(target, j, end=": ")
            if False: pr(x)
            code.append(j)
            break
# Something wrong, had to tweak this just a bit
code = [3, 0, 0, 4, 3, 14, 46, 7, 5, 6, 1, 0, 4, 6, 3, 2]
print(code)
a = 0
for x in code:
    a = (a << 3) + x
run_ = run([a , 0, 0], prog)
pr(prog)
pr(run_)
for (b, c) in zip(prog, run_):
    print(b, c)
    assert b == c
print(a)
