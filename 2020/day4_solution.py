valids = 0
keys = ["byr","iyr","eyr","hgt","hcl","ecl","pid"]
file = open('day4.input',mode='r')
for line in  file.read().split("\n\n"):
    line = line.replace("\n", " ")
    if all(key + ":" in line for key in keys):
        print(line)
        valids += 1
print(valids)
