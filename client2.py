import socket
import select
import errno
import sys
#errno is used for matching specific error codes
HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

my_username = input("Username: ")
#create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))
#the receive functionality won't be blocking
client_socket.setblocking(False)

username = my_username.encode('utf-8')
username_header = f"{len(username):<{HEADER_LENGTH}}".encode('utf-8')
#sends the username header and the username to server
client_socket.send(username_header + username)

#the only thing that won't change is the username (which we set before)
#now we will loop forever
while True:
    #this inputs text from user
    message = input(f"{my_username} > ")

    if message:
        message = message.encode('utf-8')
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode('utf-8')
        client_socket.send(message_header+message)

    try: 
        while True:
            #receive things
            username_header = client_socket.recv(HEADER_LENGTH)
            #if not len(username_header) comes into affect if we don't receive data for any reason
            if not len(username_header):
                print("connection closed by the server")
                sys.exit()
            username_length = int(username_header.decode('utf-8').strip())
            username = client_socket.recv(username_length).decode('utf-8')

            message_header = client_socket.recv(HEADER_LENGTH)
            message_length = int(message_header.decode('utf-8').strip())
            message = client_socket.recv(message_length).decode('utf-8')

            print(f"{username} > {message}")

    except IOError as e:
        #must be 'and' not 'or'
        if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
            print('Reading error', str(e))
            sys.exit()
        continue
    
    except Exception as e:
        print('General error',str(e))
        sys.exit()