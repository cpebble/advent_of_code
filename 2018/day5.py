
inputstr = "dabAcCaCBAcCcaDA"
# inputstr = "CXxRrcWhHoOwWtTwSsRApPWwar"
import sys
sys.setrecursionlimit(100000)


def reduce(stri):
    i = 0
    while i < len(stri)-1:
        cha, ncha = stri[i], stri[i+1]
        if cha.lower() == ncha.lower():
            if (cha.isupper() and ncha.islower()) or (cha.islower() and ncha.isupper()):
                # return reduce(stri[:i] + stri[i+2:])
                stri = (stri[:i] + stri[i+2:])
                i = 0
                continue
        i += 1
    return stri


if __name__ == "__main__":
    print(reduce(inputstr))
    with open("day5.input") as dinput:
        stri = dinput.read()
        print(len(stri))
        s = reduce(stri)

        print(len(s))
        minv = ("A", 9808)
        for i in "abcdefghijklmnopqrstuvwxyz":
            print("Testing char {}".format(i))
            ns = stri.replace(i, "").replace(i.upper(), "")
            ns = reduce(ns)
            print("Found of length {}".format(len(ns)))
            if len(ns) < minv[1]:
                print("New low found")
                minv = (i, len(ns))

    print(minv)

    # with open("day5.reacted", "w") as doutput:
    #     doutput.write(s)
