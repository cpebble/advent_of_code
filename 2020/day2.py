import re
#testinput = """\
#1-3 a: abcde
#1-3 b: cdefg
#2-9 c: ccccccccc
#"""
testinput = open("day2.input", "r").read()
rex = r"(\d*)-(\d*) (.): (.*)"
valid = 0
for match in re.findall(rex, testinput, re.MULTILINE):
    s = match[2]
    amount = len(re.findall(s, match[3]))
    print(str(match) + "\n" + str(int(match[0])))
    firstPos = match[3][int(match[0])-1]
    secondPos = match[3][int(match[1])-1]
    if (firstPos == s) ^ (secondPos == s):
        print(match)
        valid += 1
print(f"valid: {valid}")
