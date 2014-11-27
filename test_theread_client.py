import socket
from threading import Thread



def client(ip, port, message, response):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        # return re
        # print "Received: {}".format(response)
    finally:
        sock.close()


threads = []
responses = [{} for range(1,3)]
for i in range(1,20):
        # Create each thread, passing it its chunk of numbers to factor
        # and output dict.
        t = Thread(target=client,
                args=('127.0.0.1', 50504, "{};put;{};Testdata{}".format(i,i,i) ))
        threads.append(t)
        t.start()

results = []
for t in threads:
        t.join()

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