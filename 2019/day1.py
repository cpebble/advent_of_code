# Fuel calculations
#Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module, take its mass, divide by three, round down, and subtract 2.

# Mass 12, divide by 3 and round down to get 4. Sub 2 = 2

# We need total fuel requirement

filename = "day1.input"

total = 0

def fuel_req(mass):
    needed = mass // 3 - 2
    if needed <= 0:
        return 0
    return needed + fuel_req(needed)

with open(filename, "r") as f:
    for line in f:
        try:
            mass = int(line)
        except:
            continue
        total += fuel_req(mass)
print(total)

# Part 2
