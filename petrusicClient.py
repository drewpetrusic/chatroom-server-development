from socket import *
from threading import *

def recv_msg_handler(sock, username, addr):
    print("Congratulations {}! You are connected to the chat room server from {}.\n".format(username, str(addr)))
    while 1:
        try:
            print(sock.recv(4096).decode())
        except Exception as e:
            break



print("\nWelcome to the Chat room client program, choose a unique username to connect to the chat.\n")
while 1:
    try:
        prop_username = input("Enter username: ")
        print("")
        cl_Sock = socket(AF_INET, SOCK_STREAM)
        cl_Sock.connect(('127.0.0.1',2222))
        cl_Sock.send(prop_username.encode())
        acceptance_message = cl_Sock.recv(4096).decode()
        if acceptance_message == "user-invalid":
            print("This username is currently in use already! Pick another username...\n")
            cl_Sock.close()
            continue
        else:
            recv_msg_thread = Thread(target=recv_msg_handler, args=(cl_Sock, prop_username, cl_Sock.getsockname()))
            recv_msg_thread.start()
            break
    except Exception as e:
        print("Unable to connect to chatroom server, wait a few minutes before trying another username...\n")


while True:
    msg = input()
    cl_Sock.send(msg.encode())
