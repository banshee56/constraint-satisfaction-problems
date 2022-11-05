read_file = open('new.txt', 'r')

for line in read_file:
    line = line.replace(' ', ',')
    print(line)
print()