import socket

#A socket is just an endpoint that receives data
#With a socket you send and receive data
#It's just an endpoint that receives the communication (that sits at an IP and Port)

#AF_INET corresponds to IPV4, AF_INET = IPV4 for simpletons
#SOCK_STREAM corresponds to TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the socket to a tuple based on an IP and a Port no.
s.bind((socket.gethostname(), 1234))

#listen for incoming connections, leaving a queue of 5 (the max no.)
s.listen(5)

#listen forever for connections with a while True loop
while True:
    #anybody connects, we accept
    #store client socket object into clientsocket variable (just another socket object, like before ^)
    #store their IP in the address variable
    clientsocket, address = s.accept()

    print(f"Connection from {address} has been established!")

    #now we're sending information to the client socket
    #can send as bytes() or send a string and use the .encode method
    #utf-8 is the type of bytes we are sending
    clientsocket.send(bytes("Welcome to the server!", "utf-8"))
    clientsocket.close()