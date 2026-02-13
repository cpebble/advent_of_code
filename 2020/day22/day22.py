
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
    d1 = d1.copy()
    d2 = d2.copy()
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
        sc += i*val
    return sc

#deck = game(deck1, deck2)
#if DEBUG: print(deck)
#print(score(deck))

# Recursive
def recGame(deck1: list[int], deck2: list[int], level=0) -> tuple[int]: #, list[int], list[int]]:
    seen = set()
    round = 0
    d1 = deck1
    d2 = deck2
    while len(d1) > 0 and len(d2) > 0:
        round += 1
        if DEBUG:
            print("  "*level + f"Round [{round}], p1 deck length: {len(d1)}, p2 deck length: {len(d2)}")
            print("  "*level + f"Player 1's deck: {d1}")
            print("  "*level + f"Player 2's deck: {d2}")
        # Before either player deals a card, if there was a previous round in this
          # game that had exactly the same cards in the same order in the same players'
          # decks, the game instantly ends in a win for player 1. Previous rounds from
          # other games are not considered. (This prevents infinite games of Recursive
          # Combat, which everyone agrees is a bad idea.)
        ident = (score(d1), score(d2))
        if ident in seen:
            if DEBUG: print("  "*level + f"P1 wins game by default in")
            return (0)
        seen.add(ident)
        # Otherwise, this round's cards must be in a new configuration; the players
          # begin the round by each drawing the top card of their deck as normal.
        c1 = d1.pop(0)
        c2 = d2.pop(0)
        # If both players have at least as many cards remaining in their deck as
          # the value of the card they just drew, the winner of the round is determined
          # by playing a new game of Recursive Combat (see below).
        if len(d1) >= c1 and len(d2) >= c2:
            subd1 = d1[:c1].copy()
            subd2 = d2[:c2].copy()
            if recGame(subd1, subd2, level+1) == 0:
                d1 += [c1, c2]
                if DEBUG: print("  "*level + f"P1 wins recursive game")
            else:
                d2 += [c2, c1]
                if DEBUG: print("  "*level + f"P2 wins recursive game")
            continue

        # Otherwise, at least one player must not have enough cards left in their
          # deck to recurse; the winner of the round is the player with the higher-value
          # card.
        if c1 > c2:
            d1 += [c1, c2]
            if DEBUG: print("  "*level + f"P1 wins")
        else:
            d2 += [c2, c1]
            if DEBUG: print("  "*level + f"P2 wins")
    return int(len(d2) > 0)

gameResult = recGame(deck1, deck2) 
print(gameResult, deck1, deck2)
if gameResult == 0:
    print(score(deck1))
else:
    print(score(deck2))
