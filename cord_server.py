import socket
import threading
import SocketServer

from cord_handler import sync, check_status
from cord_processor import porcess_request


def create_logs():
    open("cord_log.log", 'a').close()
    

class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):

    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()
        response = porcess_request(data)
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass



if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = socket.gethostbyname(socket.gethostname()) , 50504

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address

    # Start a thread with the server -- that thread will then start one
    # more thread for each request
    server_thread = threading.Thread(target=server.serve_forever)
    # Exit the server thread when the main thread terminates
    create_logs()
    if sync() and check_status():
        print "All the replicas are up and synced"
        print "Server loop running in thread:", server_thread.name , ip , port
        server.serve_forever()
        server_thread.daemon = True
        server_thread.start()
        server.shutdown()
    else:
        print "We have got a problem" 
    
