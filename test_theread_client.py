import socket
from threading import Thread
REPLICA = ['192.168.1.21','129.174.55.248']

def get_seq():
    number = 5
    while True:
        yield number
        number += 1
SEQ = get_seq() 



def client(ip, port, message, response, seq):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print message
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        resp = sock.recv(1024) 
        status , message = resp.split(';')
        from_srv = {'ip': ip ,
                    'seq':seq ,
                    'status':status, 
                    'message':message}
        response.append( from_srv )
    finally:
        sock.close()
    return True


threads = []
responses = [[] for i in range (len(REPLICA) ) ]
seq = SEQ.next()
for i in range(len(REPLICA)):
        print REPLICA[i], i
        t = Thread(target=client,
                args=(REPLICA[i], 50504, "{};put;{};Testdata{}".format(seq,i,i), responses[i] , seq)  )
        threads.append(t)
        t.start()
results = []
for t in threads:
        t.join()

# print responses

if all(message[0]['status'] == 'True'  for message in responses):
    commit_reponses = [[] for i in range(len(responses)) ]
    commit_threads = []
    for i in range(len(responses)):
        t = Thread(target=client,
                    args=(REPLICA[i], 
                        50504, "{};com;;".format(responses[i][0]['seq']), 
                        responses[i] , 
                        seq
                    ))
        commit_threads.append(t)
        t.start()

for t in commit_threads:
        t.join()



print commit_reponses

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