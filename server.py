import socket, select

#FUNCTION STARTS

def dataReceived(client_socket):
    try:
        data_header = client_socket.recv(header_len)

        if not len(data_header):
            return False
        
        data_length = int(data_header.decode('utf-8').strip())
        #returns a dict
        return {"header" : data_header, "data" : client_socket.recv(data_length)}
    except:
        return False

#FUNCTION ENDS

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

ip = socket.gethostbyname(socket.gethostname()) 
port = 8080
header_len = 10

print(f"[*] Connect to server with IP Address: {ip} and Port: {port}")

server_socket.bind((ip, port))
server_socket.listen(2)

sockets_list = [server_socket]
clients = {}

while True:
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)
    
    #print("read sockets: ", read_sockets)

    for x in read_sockets:
        if x == server_socket:
            client_socket, client_address = server_socket.accept()

            #setting user data equal to (a dictionary with two values: 'data header', and 'data') return value of dataReceived function 
            #i think it's called user because this is meant to be used for the intial username data
            user = dataReceived(client_socket)

            if user is False:
                continue

            sockets_list.append(client_socket)
            #print("sockets list: ", sockets_list)

            clients[client_socket] = user
            #print("client socket: ", user)

            print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username: {user['data'].decode('utf-8')}")

        else:
            data = dataReceived(x)

            if data is False:
                print(f"Closed connection from {clients[x]['data'].decode('utf-8')}")
                sockets_list.remove(x)
                del clients[x]
                continue

            user = clients[x]

            print(f"Received data from {user['data'].decode('utf-8')}: {data['data'].decode('utf-8')}")

            for client_socket in clients:
                #we don't want to send the message back to the sender
                if client_socket != x:
                    client_socket.send(data['header'] + data['data'])

    for x in exception_sockets:
        sockets_list.remove(x)
        del clients[x]



