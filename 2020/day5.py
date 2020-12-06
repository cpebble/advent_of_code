from math import ceil, floor

maxi = 0
seats = [0]*971
with open("day5.input") as fil:
    for ticket in fil.readlines():
        text = ticket.strip()
        inp = text[:7]
        inp_ = text[-3:]

        low = 0
        high = 127
        for i in inp:
            if i == "F":
                high = low+(ceil((high-low) // 2))
            elif i == "B":
                low = low+ceil((high-low) // 2)
        left = 0
        right = 7
        for i in inp_:
            if i == "L":
                right = left+((right-left) // 2)
            elif i == "R":
                left = left+((right-left) // 2) + 1
        sid = high*8+right
        if sid > maxi: maxi = sid
        print(f"id is {high*8+right}")
        seats[sid] += 1

for i in range(2, len(seats) - 1):
    if seats[i-1] == 1 and seats[i+1] == 1 and seats[i] == 0:
        print(i)
print(maxi)
