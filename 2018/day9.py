
def placeMarble(marbles, current_marble, player, marble):
    newMarbles = []
    scoreChange = 0
    marble_index = 0
    if marble % 23 == 0:
        scoreChange += marble
        marble2 = (current_marble - 7) % len(marbles)
        scoreChange += marbles[marble2]
        del marbles[marble2]
        marble_index = marble2 % len(marbles)
        newMarbles = marbles
    else:
        marble_index = (current_marble + 2) % len(marbles)
        newMarbles = insertAtIndex(marbles, marble_index, marble,)
    return newMarbles, marble_index, scoreChange


def insertAtIndex(arr, index, elem):
    slice1, slice2 = arr[:index], arr[index:]
    new_arr = slice1 + [elem] + slice2
    return new_arr


def printMarbles(player, marbles, current):
    print("[{}]".format(player+1), end="")
    for i in range(len(marbles)):
        if i == current:
            print("*{} ".format(marbles[i]), end="")
        else:
            print(" {} ".format(marbles[i]), end="")
    print()


# Puzzle_input: 459 players; last marble is worth 71320 points
if __name__ == "__main__":
    playerCount = 459
    players = [0 for i in range(playerCount)]
    marbles = [0, 1]
    highest_marble = 71320
    player = 1
    current_marble = 1

    for i in range(1, highest_marble):
        marbles, current_marble, score = placeMarble(
            marbles,
            current_marble,
            player,
            i+1
        )
        # printMarbles(p[kklayer, marbles, current_marble)
        players[player] += score
        player = (player + 1) % playerCount

    print(max(players))
