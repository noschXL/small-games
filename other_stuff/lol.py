import random

map = [ [0 for _ in range(5)] for _ in range(5)]

# define start
map[0][3] = 2
#define end
map[4][3] = 3

for i in range(5):
    print(str(map[i]))