import re

inp = open("day8.input").read()

instrs = list(re.findall(r"(\w\w\w) ([+-]\d+)", inp))
#print(instrs)

running = True

def parse_code(instrSet, shouldBranch, _pc=0, _acc=0):
    visited = set()
    acc = _acc
    pc = _pc
    while pc not in visited and pc < len(instrSet):
        visited.add(pc)
        ins, arg = instrSet[pc]
        print(f"[{pc:3}, {acc:3}] {ins} {arg}")
        if ins == "nop":
            pc += 1
        elif ins == "acc":
            acc += int(arg)
            pc += 1
        elif ins == "jmp":
            if shouldBranch:
                # Create a new reality
                print(f"Branching on op {pc}")
                instrSet[pc] = ("nop", arg)
                ret, _acc = parse_code(instrSet, False, pc, acc)
                if ret:
                    print(f"Loop terminated by changing nop: {pc}. Acc is {_acc}")
                    return (ret, acc)
                else:
                    instrSet[pc] = ("jmp", arg)
            pc += int(arg)

    return (pc == len(instrSet), acc)

parse_code(instrs, True)
