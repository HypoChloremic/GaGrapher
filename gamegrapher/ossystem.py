import os

with open("random.txt", 'w') as file:
    file.write(str(os.system("tasklist")))
