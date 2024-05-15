import socket
import os

class SimpleHTTPServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def serve_forever(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print("Server running on http://{}:{}".format(self.host, self.port))

        try:
            while True:
                client_sock, client_addr = self.sock.accept()
                self.handle_client(client_sock)
        except KeyboardInterrupt:
            self.shutdown()

    def handle_client(self, client_sock):
        request = client_sock.recv(1024)
        if not request:
            return
        method, path, _ = request.split(' ', 2)
        if method != 'GET':
            client_sock.sendall("HTTP/1.1 405 Method Not Allowed\r\n\r\n")
            client_sock.close()
            return
        if path == '/':
            path = 'index.html'
        else:
            path = path.lstrip('/')
        if not os.path.exists(path):
            client_sock.sendall("HTTP/1.1 404 Not Found\r\n\r\n")
            client_sock.close()
            return
        with open(path, 'rb') as f:
            response_data = f.read()
            response = "HTTP/1.1 200 OK\r\nContent-Length: {}\r\n\r\n{}".format(len(response_data), response_data)
            client_sock.sendall(response)
        client_sock.close()

    def shutdown(self):
        print("Shutting down the server")
        self.sock.close()

if __name__ == "__main__":
    server = SimpleHTTPServer('localhost', 8090)
    server.serve_forever()
