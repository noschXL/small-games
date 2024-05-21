import secrets
import os

path = os.path.dirname(os.path.abspath(__file__))



file = open(os.path.join(path, 'password.txt'), 'r')
content = file.read()
file.close()
print(content)

free = False
line = 0
file = open(os.path.join(path, 'password.txt'), 'r')

while not free:
    content_line = file.readline()
    if content_line == '':
        free = True
    line += 1

file.close()

file = open(os.path.join(path, 'password.txt'), 'a')
file.writelines("\nnoschXL : abc123")
file.close()
print(line)