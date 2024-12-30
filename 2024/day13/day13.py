from functools import cache
import re
import numpy as np
prod = True
inp = """\
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""

with open('input') as f:
    if prod: 
        inp = f.read()
        inp.strip()

inp = inp.split("\n\n")

def naivewinmachine(machine):
    try:
        ba, bb, prize = machine.strip().split("\n")
    except:
        breakpoint()
        return None
    ax, ay = re.match(r"Button .: X\+(\d*), Y\+(\d*)", ba).groups()
    bx, by = re.match(r"Button .: X\+(\d*), Y\+(\d*)", bb).groups()
    px, py = re.match(r"Prize: X=(\d*), Y=(\d*)", prize).groups()
    ax,ay,bx,by,px,py = int(ax),int(ay),int(bx),int(by),int(px),int(py)
    cheapest = None
    for i in range(100):
        for j in range(100):
            if i*ax + j*bx == px and i*ay + j*by == py:
                if cheapest == None or i*3+j < cheapest:
                    cheapest = i*3+j
    return cheapest


def winmachine(machine, eps=0.0000001):
    ba, bb, prize = machine.strip().split("\n")
    ax, ay = re.match(r"Button .: X\+(\d*), Y\+(\d*)", ba).groups()
    bx, by = re.match(r"Button .: X\+(\d*), Y\+(\d*)", bb).groups()
    px, py = re.match(r"Prize: X=(\d*), Y=(\d*)", prize).groups()
    ax,ay,bx,by,px,py = int(ax),int(ay),int(bx),int(by),int(px),int(py)
    A = np.array([[ax, bx], [ay, by]])
    b = np.array([px + 10000000000000, py + 10000000000000])
    A_ = np.linalg.inv(A)
    x = np.matmul(A_, b)
    print("SOL")
    a, b = round(x[0]), round(x[1])
    if ((a*ax + b*bx == px +10000000000000 )) and\
        ((a*ay + b*by == py +10000000000000 )):
        return a*3 + b
    else:
        return None
    # Equation 
    # i*ax + j*bx = px
    # i*ay + j*by = py


mcost = 0
for m in inp:
    cost = winmachine(m, 0.000001)
    if cost != None:
        mcost += cost
print(mcost)
