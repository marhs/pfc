import socketserver
import json

class Server(socketserver.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        if len(self.data) == 0:
            print('Nada')
        print("{} wrote:".format(self.client_address[0]))
        jdata = self.data.decode()
        jdata = json.loads(jdata)
        print(jdata['holo'])
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())



if __name__ == "__main__":
    HOST, PORT = "localhost", 30000

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), Server)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
