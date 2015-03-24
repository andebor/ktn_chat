# -*- coding: utf-8 -*-
import SocketServer
import json


class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    BUFFER_SIZE = 4096

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request

        print 'Client connected with hostname ' + self.ip + ':' + str(self.port)

        try:
            while True:
                received_string = json.loads(self.connection.recv(BUFFER_SIZE))
                if not received_string:
                    break

                request = received_string["request"]

                if(request == "login"):
                    self.username = received_string["content"]
                    response = self.login()
                elif(request == "logout"):
                    reponse = self.logout()
                elif(request == "message"):
                    msg = request["content"]
                    reponse = self.message(msg)
                elif(request == "names"):
                    reponse = self.names()
                elif(request == "help"):
                    response = self.help()

                print "response: " + response
                print "users: " + Server.users
                self.send(response)
        except:
            pass



            
            # TODO: Add handling of received payload from client

    def login(self):
        response = {'response': 'login', 'content': self.username }

        if self.username in Server.users:
            response["error"] = "User already logged in"
        else:
            server.users[self.username] = self.request

        return response

    def logout(self):
        response = {'response': 'logout', 'content': self.username }
        return response

    def message(self, message):
        response = {'response': 'message', 'content': message }
        return


    def names(self):
        reponse = {'response': 'names'}
        reponse["content"] = str(Server.users)
        return reponse

    def help(self):
        response = {'response': 'help'}
        reponse['content'] = """
        login <username> - log in with the given username 
        logout - log out
        msg <message> - send message
        names - list users in chat
        help - view help text
        """
        return reponse



    def send(self, data):
        for user in Server.users:
            server.users[username].sendall(json.dumps(data))


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    def init(self):
        self.users = {}

    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations is necessary
    """
    allow_reuse_address = True




if __name__ == "__main__":
    """
    This is the main method and is executed when you type "python Server.py"
    in your terminal.

    No alterations is necessary
    """
    HOST, PORT = 'localhost', 9997
    print 'Server running...'

    # Set up and initiate the TCP server
    server = ThreadedTCPServer((HOST, PORT), ClientHandler)
    server.serve_forever()
