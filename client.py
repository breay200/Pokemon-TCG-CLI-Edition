import socket

HEADERSIZE = 10

#Uses the exact same socket as the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#instead of binding (like with the server) we connect
#parameters are a tuple of the IP and the Port we want to connect to
#in most cases we're not going to use socket.gethostname(), we'll connect to a public IP or a local IP
s.connect((socket.gethostname(), 1234))

while True:
    full_msg = ""
    new_msg = True
    while True:
        #remember that the TCP socket (SOCK_STREAM) is a stream of data
        #we need to decide how big the chunks of data we will receive at a time
        #for example: if you're sending files then you'll want something larger, application you're going to use it with...
        #1024 is the buffer size
        #msg = s.recv(1024)

        #test
        msg = s.recv(16)

        if new_msg:
            print(f"new message length {msg[:HEADERSIZE]}")
            msglen = int(msg[:HEADERSIZE])
            new_msg = False
        
        full_msg += msg.decode("utf-8")

        if len(full_msg)-HEADERSIZE == msglen:
            print("full msg received")
            print(full_msg[HEADERSIZE:])
            new_msg = True
            full_msg = ""
    
    print(full_msg)
        #decodes message
        #what we're using is a byte stream, so the data is sent as bytes, recieved as bytes
        #therefore we need to encode and decode the messages
        #print(msg.decode("utf-8"))