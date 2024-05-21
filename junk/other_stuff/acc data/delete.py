import os 

path = os.path.dirname(os.path.abspath(__file__))

os.remove(os.path.join(path, 'password.password'))