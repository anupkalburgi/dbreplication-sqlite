import socket
from threading import Thread



def client(ip, port, message, response):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print message
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response.append (sock.recv(1024))
        # return re
        # print "Received: {}".format(response)
    finally:
        sock.close()
    return True


REPLICA = ['129.174.126.30','129.174.55.248']

threads = []
responses = [[] for i in range (len(REPLICA) ) ]
for i in range(len(REPLICA)):
        # Create each thread, passing it its chunk of numbers to factor
        # and output dict.
        print REPLICA[i], i
        t = Thread(target=client,
                args=(REPLICA[i], 50504, "{};put;{};Testdata{}".format(i+1,i+1,i+1), responses[i] )  )
        threads.append(t)
        t.start()

results = []
for t in threads:
        t.join()

print responses

# for i in range(1,20):
#     thread = Thread(target = client, args = ('127.0.0.1', 50504, "{};abort;;".format(i) ))


#     #thread = Thread(target = client, args = ('127.0.0.1', 50504, "{};com;;".format(i) ))
    
#     # thread = Thread(target = client, args = ('127.0.0.1', 50504, ";get;{};".format(i) ))
#     # thread = Thread(target = client, args = ('127.0.0.1', 50504, "{};del;{};".format(i+1,i) ))
#     thread.start()
#     thread.join()

# client('127.0.0.1', 55218, "Hello World 1")
# client('127.0.0.1', 55218, "Hello World 2")
# client('127.0.0.1', 55218, "Hello World 3")