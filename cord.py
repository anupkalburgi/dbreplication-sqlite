import socket
REPLICA = ['192.168.1.21','129.174.55.248']



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
    except socket.error, v:
        errorcode=v[0]
        if errorcode==errno.ECONNREFUSED:
            logger.error("connection_refused:{}".format(ip))
            from_srv = {'ip': ip ,
                    'seq':seq ,
                    'status':'False', 
                    'message':'Cound not connect to server'}
            response.append( from_srv )
    finally:
        sock.close()
    return True