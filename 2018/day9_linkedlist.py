import tqdm


class Marble():
    def __init__(self, value, *args, **kwargs):
        self.left = None
        self.right = None
        self.value = value

    def clockwise(self, amount=2):
        cur = self
        for i in range(amount):
            cur = cur.right
        return cur

    def counter_clockwise(self, amount=2):
        cur = self
        for i in range(amount):
            cur = cur.left
        return cur


def placeMarble(current_marble, value):
    scoreChange = 0
    if value % 23 == 0:
        # We keep our marble
        scoreChange += value
        # Find the marble 7 cw
        marble_to_remove = current_marble.counter_clockwise(7)
        # Do linked-list removal
        marble_to_remove.left.right = marble_to_remove.right
        marble_to_remove.right.left = marble_to_remove.left
        # Add removed marble to score
        scoreChange += marble_to_remove.value
        # Current marble
        marble = marble_to_remove.right
        # Delete object
        del marble_to_remove
    else:
        marble = Marble(value)
        # Go 2 clockwise
        insert = current_marble.clockwise(2)
        # Linked_list insertion
        tmp = current_marble.clockwise(1)
        insert.left = marble
        marble.right = insert
        tmp.right = marble
        marble.left = tmp
        # Return
    return marble, scoreChange


def insertAtIndex(arr, index, elem):
    slice1, slice2 = arr[:index], arr[index:]
    new_arr = slice1 + [elem] + slice2
    return new_arr


def printMarbles(player, marble):
    print("[{}]".format(player+1), end="")
    print("*{} ".format(marble.value), end="")
    init = marble
    marble = marble.clockwise(1)
    while marble != init:
        print(" {} ".format(marble.value), end="")
        marble = marble.clockwise(1)
    print()


# Puzzle_input: 459 players; last marble is worth 71320 points
if __name__ == "__main__":
    playerCount = 459
    players = [0 for i in range(playerCount)]
    highest_marble = 71320*100
    player = 0
    current_marble = Marble(0)
    current_marble.left = current_marble
    current_marble.right = current_marble

    for i in tqdm.tqdm(range(0, highest_marble)):
        current_marble, score = placeMarble(current_marble, i+1)

        # printMarbles(player, current_marble)
        players[player] += score
        player = (player + 1) % playerCount

    print(max(players))
