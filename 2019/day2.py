## opcode parser

def parse_opcode(opcode):
    if opcode == 2:
        return "multiply", 4
    if opcode == 1:
        return "add", 4
    if opcode == 99:
        return "halt", 1
    return "error"

def run(program):
    pc = 0
    while(True):
        opcode, offset = parse_opcode(program[pc])
        if opcode == "error":
            print("Got error at pos {} with opcode {}".format(pc, program[pc]))
            break
        if opcode == "halt":
            print("Halt reached")
            break

        # Get arguments
        arg1_p = program[pc+1]
        arg1 = program[arg1_p]
        arg2_p = program[pc+2]
        arg2 = program[arg2_p]
        dst_p = program[pc+3]
        
        result = arg1 + arg2 if opcode == "add" else arg1 * arg2

        program[dst_p] = result
        
        pc += offset
    return 0

running = True
program_clean = []
# Load program into memory
with open("day2.input") as f:
    program_clean = [int(s) for s in f.readline().split(",")]

for i,j in [(i,j) for i in range(100) for j in range(100)]:
    program = program_clean.copy()
    # Restore state:
    program[1] = i
    program[2] = j
    pc = 0

    status = run(program)
    
    if program[0] == 19690720:
        print(i,j)
        break
    else:
        pass
        print("Tried {},{} with res:{}".format(i,j,program[0]))


