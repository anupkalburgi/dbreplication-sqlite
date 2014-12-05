from threading import Thread
import socket

IP = "10.159.22.182"
port = 50504
def client(message, response, seq=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((IP, port))
        sock.sendall(message)
        resp = sock.recv(1024) 
        status , message = resp.split(';')
        from_srv = {'server': IP ,
                    'seq':seq ,
                    'status':status, 
                    'message':message}
        response.append( from_srv )
    except socket.error, v:
        errorcode=v[0]
        logger.error("connection_refused:{}".format(ip))
        from_srv = {'server': ip ,
                    'seq':seq ,
                    'status':'False', 
                    'message':'Cound not connect to server'}
        response.append( from_srv )
        return True
    finally:
        sock.close()
    return True


DATA = [(913,"Testing replication"),(112,"Concurrent"),(214,"Not fault tollerent"),(219,"and my attept")]
# response = []
# client("put;2;ccmdn",response )
threads = []
get_threads = []
del_threads = []
responses = [[] for i in range (len(DATA) ) ]
get_responses = [[] for i in range (len(DATA) ) ]
del_responses = [[] for i in range (len(DATA) ) ]

for i in range(len(DATA)):
        t = Thread(target=client,args=( "put;{};{}".format( DATA[i][0],DATA[i][1] ) , responses[i] ) )
        t1 = Thread(target=client,args=( "get;{};".format( DATA[i][0] ) , get_responses[i] ) )
        t2 = Thread(target=client,args=( "del;{};".format( DATA[i][0] ) , del_responses[i] ) )
        threads.append(t)
        get_threads.append(t1)
        del_threads.append(t2)
        t.start()
        t1.start()
        t2.start()

for t in threads:
        t.join()
for t in get_threads:
        t.join()
for t in del_threads:
        t.join()

print responses
print get_responses
print del_responses