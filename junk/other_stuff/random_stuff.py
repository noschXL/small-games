import random
string = ""
letters = "abcdefghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!§$%&/()=ß?"
for i in range(8):
    string += random.choice(letters)
print(string)