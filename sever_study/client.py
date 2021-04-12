import socket

PORT = 5050
HEADER = 64
FORMAT = 'utf-8'
DISSCONNECT_MSG = 'dissconnect!'

SERVER = socket.gethostbyname(socket.gethostname())   # get IPv4 automatically for you
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)   # encode from utf-8 to bytes
    
    # make sure the first message we sent is 64 bytes long. (HEADER = 64)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))   # pad the string to 64 bytes

    # send the message
    client.send(send_len)
    client.send(message)

    print(client.recv(2048).decode(FORMAT))

send("I miss you red!")
send(DISSCONNECT_MSG)
