import sys

# sort results.txt
f = open("results.txt", "r")
lines = f.readlines()
f.close()

lines.sort()

# remove number from any line that starts with a number
for i in range(len(lines)):
    try:
        parts = lines[i].split(" ")
        t = float(parts[0])
        lines[i] = " ".join(parts[1:])
    except:
        pass

# write back to the file.
f = open("results.txt", "w")
for line in lines: f.write(line)
f.close()
