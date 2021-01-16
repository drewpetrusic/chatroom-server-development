from socket import *
from threading import *

clients = {}

def client_handler(username, addr):
    while 1:
        try:
            msg = clients[username][1].recv(4096).decode()
            broadcast_msg = '<{}> {}'.format(username, msg)
            print(broadcast_msg)
            for client in clients:
                clients[client][1].send(broadcast_msg.encode())
        except Exception as e:
            disconnect_msg = '<{}> has disconnected from the chat server.'.format(username)
            clients[username][1].close()
            del clients[username]
            for client in clients:
                clients[client][1].send(disconnect_msg.encode())
            break



sr_Sock = socket(AF_INET, SOCK_STREAM)
sr_Sock.bind(('127.0.0.1', 2222))
sr_Sock.listen(5)
print("\nChatroom Server is ready to accept new connections on " + str(sr_Sock.getsockname()))

while 1:
    try:
        cn_Sock, addr = sr_Sock.accept()
        cl_username = cn_Sock.recv(4096).decode()
        for client in clients:
            if client == cl_username:
                cn_Sock.send("user-invalid".encode())
                cn_Sock.close()
                continue
        cn_Sock.send("user-valid".encode())
        cl_thread = Thread(target=client_handler, args=(cl_username, addr))
        clients[cl_username] = [cl_thread, cn_Sock]
        cl_thread.start()
        joined = '<{}> has connected to the chat server.'.format(cl_username)
        print(joined)
        for client in clients:
            clients[client][1].send(joined.encode())
    except Exception as e:
        continue
