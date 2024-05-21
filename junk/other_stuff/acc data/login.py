import os
import sys

path = os.path.dirname(os.path.abspath(__file__))
try:
    file = open(os.path.join(path, 'password.password'), 'r')
except FileNotFoundError as e:
    print("file not found: 'password.password' . Maybe it doesn't exist?")
    sys.exit()

name = input("username: ")
password = input("password: ")


file = open(os.path.join(path, 'password.password'), 'r')

end = None
found = False
while True:
    line = file.readline()
    if line == '':
        break

    for i in range(len(line)):
        if line[i] == ":":
            end = i

    if name == line[:end].strip():
        found = True
        if password == line[end + 1:].strip():
            print("hallo " + name.strip())
        else:
            print("wrong password")

if not found:
    print("no matching username was found")

file.close()