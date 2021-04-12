import os

# filepath = './pastebot.net'
filename = 'f3.txt'
filepath = os.path.join("pastebot.net", filename)
f = open(filepath, 'wb')
f.write(b"success")
f.close()