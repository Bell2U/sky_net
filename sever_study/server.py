import socket
import threading
import pickle  # pickle a object into string to send it through the net

# reference https://www.youtube.com/c/TechWithTim/search?query=Python%20Socket%20Programming%20Tutorial

PORT = 5050
SERVER = "192.168.0.108"    # run ipconfig in cmd, and find the IPv4 address, which is your local ip address.
SERVER = socket.gethostbyname(socket.gethostname())   # get IPv4 automatically for you
ADDR = (SERVER, PORT)
HEADER = 64
FORMAT = 'utf-8'
DISSCONNECT_MSG = 'dissconnect!'

# socket.socker(family, standard operation)
# family: indecates which type of ip address that gonna been selected by the server.
# standard operation: the way of sending data through sockets
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # make a new socket

# bind the address to the socket, any thing that connected to the address will hit the socket.
server.bind(ADDR)

def handle_client(conn, addr):
    print(f'[new connection] {addr} connected')

    connected = True
    while connected:
        # wile connected, wait for information from the client.
        # define how many bytes we receive each time from a block
        msg_len = conn.recv(HEADER).decode(FORMAT)  # this line will wait until someting is sent over the socket
        if msg_len:
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)

            if msg == DISSCONNECT_MSG:
                connected = False

            print(f'[{addr}] {msg}')

            conn.send("I got your message".encode(FORMAT))

    # close the current connection
    conn.close()

def start():
    # linsen a new connection
    server.listen()
    print(f'[linsening] server is linsening on {SERVER}')

    # wait for a new connection to the server
    while True:
        conn, addr = server.accept()    # a new connection occurse, this line will waits until find a new connection.
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        # print the total number of connections currently run.
        # we have to minus one, because the main thread is always active.
        print(f'[active connections] {threading.active_count() - 1}')

print("server starting...")
start()
