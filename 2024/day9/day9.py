from queue import Queue
prod = True

inp = """\
2333133121414131402"""
with open('input') as f:
    if prod: 
        inp = f.read()

inp = inp.strip()


files = []
freespace = []
fullmap = []
for i in range(len(inp)):
    x = int(inp[i])
    if i % 2 == 0:
        files += [(x, i // 2)]
        fullmap+= [i // 2] * x
    else:
        freespace += [x] 
        fullmap += [-1]*x

#print(files)
#print(freespace)
#print(fullmap)
def part1(files, freespace):
    compacted = []
    i = 0
    while True:
        # Break Case
        if files[i][0] == 0:
            break
        # Fill in file
        compacted += [files[i][1]]*files[i][0]
        files[i] = (0, files[i][1])
        # Fill in free space
        for j in range(freespace[i]):
            # Get a block
            k = -1
            try:
                while files[k][0] == 0:
                    k -= 1
            except IndexError:
                break
            compacted.append(files[k][1])
            files[k] = (files[k][0] - 1, files[k][1])

        i += 1
    part1 = 0
    for (i, fid) in enumerate(compacted):
        part1 += i*fid
    print(part1)
    return compacted

#part1(files, freespace)
def part2(fmap):
    tried = set()
    for i in range(len(fmap)-1, 0, -1):
        # First, find the file we want
        c = fmap[i]
        # Ignore free space
        if c == -1 or c in tried:
            continue
        tried.add(c)

        # Count blocks
        n = 1
        while i-n >= 0 and fmap[i-n] == c:
            n+=1

        # Find free space
        j = 0
        m = 0
        while m < n and j < len(fmap):
            if fmap[j] == -1:
                m += 1
            else:
                m = 0
            j += 1
        j = j-m
        if j < i:
            for k in range(n):
                fmap[j + k] = c
                fmap[i - k] = -1
            #print(f"Found {n} blocks for {c} at {j-m}")
        else:
            pass #print(f"Couldn't find space for {c}")
    #print(fmap)
    return fmap

        

fmap = part2(fullmap)
print(sum([i*c for i, c in enumerate(fmap) if c != -1]))

