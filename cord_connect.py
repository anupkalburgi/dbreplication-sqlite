import socket
REPLICA = ['192.168.1.21','129.174.55.248']
port = 50504

import logging
logger = logging.getLogger('cord_log')
hdlr = logging.FileHandler('cord_log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)

def client(ip, message, response, seq=None):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        sock.sendall(message)
        resp = sock.recv(1024) 
        status , message = resp.split(';')
        from_srv = {'server': ip ,
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