#handling multiple connections on serverside
import socket
#select gives us operating system level I/O capabilities but with sockets in mind
import select


HEADER_LENGTH = 10
IP = "127.0.0.1"
PORT = 1234

#AF_INET is type of socet (address family internet)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#code below allows us to reconnect to port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#bind as usual the IP and Port (like before)
server_socket.bind((IP, PORT))

server_socket.listen()

#now we need to manage the list of sockets (clients)
#we need to add the server to the list
#as clients connect, we'll add them to the socket_list
sockets_list = [server_socket]

clients = {}

def receive_message(client_socket):
    try:
        message_header = client_socket.recv(HEADER_LENGTH)

        if not len(message_header):
            return False
        
        message_length = int(message_header.decode("utf-8").strip())
        return {"header" : message_header, "data" : client_socket.recv(message_length)}
    
    except:
        return False

while True:
    #select.select takes 3 parameters: the read list (the things you wanna read in), the write list, sockets we might error on  
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    for notified_socket in read_sockets:
        #this means someone just connected and we need to accept this connection and also just handle for it
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()

            user = receive_message(client_socket)
            #if user just disconnected
            if user is False:
                continue
            
            #appending the client to the socket list
            sockets_list.append(client_socket)

            #this is the current information we have on this client socket 
            clients[client_socket] = user

            #used for if someone just connected
            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

        else:
            message = receive_message(notified_socket)

            if message is False:
                print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]
                continue

            user = clients[notified_socket]
            
            
            print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

            for client_socket in clients:
                #we don't want to send the message back to the sender
                if client_socket != notified_socket:
                    client_socket.send(user['header'] + user['data'] + message['header'] + message['data'])
    
    for notified_socket in exception_sockets:
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
