# Find two entries that sum together to produce 2020

#testinput = [
        #1721,
        #979,
        #366,
        #299,
        #675,
        #1456
#]
testinput = []
with open("day1.input") as inp:
    for line in inp.readlines():
        testinput += [int(line)]

i = 0
while(i < len(testinput)):
    j = i
    cur = testinput[i]
    while(j < len(testinput)):
        curj = testinput[j]
        k = 0
        if cur + curj >= 2020:
            j += 1
            continue
        while (k < len(testinput)):
            curk = testinput[k]
            if (cur + curj + curk) == 2020:
                print(f"Got match on {cur} and {curj} and {curk}.\n" +
                      f"The multiple is {cur * curj * curk}")
            k += 1
        j+= 1
    i+=1
    print(f"I is now: {i}")

