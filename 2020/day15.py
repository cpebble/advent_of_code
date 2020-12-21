from collections import Counter

starting = [3, 1, 2]
starting = [0,1,5,10,3,12,19]


numbers = Counter()


lastsaid = 0

for i in range(len(starting) - 1):
    numbers[starting[i]] = i + 1

lastsaid = starting[-1]
i = len(starting) + 1
while i <= 30000000:
    if numbers[lastsaid] == 0:
        # Never said before
        #print(f"[{i}] Number {lastsaid} never said before")
        numbers[lastsaid] = i - 1
        lastsaid = 0
    elif numbers[lastsaid] >= 0:
        a = numbers[lastsaid]
        #print(f"[{i}] Number {lastsaid} said on turn {a}, saying {(i-1-a)}")
        numbers[lastsaid] = i - 1
        lastsaid = (i-1-a)

    i += 1
print(lastsaid)
