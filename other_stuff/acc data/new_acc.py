import os

path = os.path.dirname(os.path.abspath(__file__))

file = open(os.path.join(path, 'password.password'), 'a')
file.close()

file = open(os.path.join(path, 'password.password'), 'r')

name = input("whats your name? ")
password = input("and whats your password? ")

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

file.close()
file = open(os.path.join(path, 'password.password'), 'a')

if not found:
    file.writelines("\n" + name + ":" + password)
else:
    print("someone already made an account with that username")