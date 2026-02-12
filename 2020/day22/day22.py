
TEST = False
DEBUG = False
inp = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""

with open("day22.input") as f:
    realin = f.read()

inp: str = realin if not TEST else inp

player1, player2 = inp.split("\n\n")
deck1 = list(map(int, player1.splitlines()[1:]))
deck2 = list(map(int, player2.splitlines()[1:]))

print(deck1, deck2)

def turn(d1: list[int], d2: list[int]) -> tuple[list[int], list[int]]:
    c1 = d1.pop(0)
    c2 = d2.pop(0)
    if c1 > c2:
        return (d1 + [c1, c2], d2)
    else:
        return (d1, d2 + [c2, c1])


def game(d1: list[int], d2: list[int]) -> list[int]:
    i = 0
    while len(d1) > 0 and len(d2) > 0:# and i <= 3000000:
        d1, d2 = turn(d1, d2)
        i += 1
        if DEBUG: print(f"Round [{i}], p1 deck length: {len(d1)}, p2 deck length: {len(d2)}")
        if DEBUG:
            print(f"Player 1's deck: {d1}")
            print(f"Player 2's deck: {d2}")
    if len(d1) == 0:
        return d2
    elif len(d2) == 0:
        return d1
    else: raise Exception(f"ran {i}")

def score(d: list[int]) -> int:
    sc = 0
    for i, val in zip(d, range(len(d), 0, -1)):
        if DEBUG: print(i, val)
        sc += i*val
    return sc

deck = game(deck1, deck2)
if DEBUG: print(deck)
print(score(deck))

