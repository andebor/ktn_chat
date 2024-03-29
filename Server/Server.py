# -*- coding: utf-8 -*-
import SocketServer
import json
import re
import traceback
from datetime import datetime

# Server response skal være i følgende format: 
#{
#    ‘timestamp’: <timestamp>,
#    ‘sender’: <username>,
#    ‘response’: <response>,
#    ‘content’: <content>
#}
# Response types: error, info, history and message
BUFFER_SIZE = 4096

log = []

class ClientHandler(SocketServer.BaseRequestHandler):
    """
    This is the ClientHandler class. Everytime a new client connects to the
    server, a new ClientHandler object will be created. This class represents
    only connected clients, and not the server itself. If you want to write
    logic for the server, you must write it outside this class
    """

    

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        self.loggedIn = False
        self.username = ''

        print 'Client connected with hostname ' + self.ip + ':' + str(self.port)

        try:
            while True:
                received_string = json.loads(self.connection.recv(BUFFER_SIZE).strip())
               # if not received_string:
                    #break

                print ""
                print "Serveren mottok data:"
                for key, value in received_string.iteritems():
                    print str(key) + ": " + str(value)




                request = received_string["request"]
                response = {}
                hist = {}

                if(request == "login"):
                    self.username = received_string["content"]
                    response = self.login()
                    hist = self.history()
                elif(request == "logout"):
                    response = self.logout()
                elif(request == "msg"):
                    msg = received_string["content"]
                    response = self.message(msg)
                elif(request == "names"):
                    response = self.names()
                elif(request == "help"):
                    response = self.help()
                else:
                    print "unknown request"

                print ""
                print "Serveren sender data: "
                for key, value in response.iteritems():
                    print str(key) + ": " + str(value)


                self.send(response)

                if hist != {}:
                    self.send(hist)
        except Exception,e:
            print traceback.format_exc()
            pass
            



            
            # TODO: Add handling of received payload from client

    def login(self):
        response = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sender': self.username,
            'response': 'info',
            'content': self.username + ' logged on.'
            }

        if self.username in server.users:
            response['response'] = 'error'
            response['content'] = self.username + ' is already logged in.'
        elif self.loggedIn == True:
            response['response'] = 'error'
            response['content'] = "You are already logged in"
        elif re.match("^[a-zA-Z0-9]+$", self.username) is None:
            response['response'] = 'error'
            response['content'] = self.username + ' Only alphabethic character and numbers are accepted in username'
        else:
            server.users[self.username] = self.request
            self.loggedIn = True

        return response

    def logout(self):
        response = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sender': "",
            'response': 'info',
            'content': self.username + ' logged off.'
            }
        if self.loggedIn == False:
            response['response'] = 'error'
            response['content'] = "Can't log out because you are not logged in"
        else:
            self.loggedIn = False
            self.server.users.pop(self.username)

        if self.username:
            response['sender'] = self.username
        return response

    def message(self, message):
        response = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sender': "",
            'response': 'message',
            'content': message
            }
        if self.loggedIn == False:
            response['response'] = 'error'
            response['content'] = "You need to be logged in to send messages"
        if self.loggedIn == True:
            log.append(self.username + ": " + message)
            response['sender'] = self.username
        return response


    def names(self):
        response = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sender': "",
            'response': 'info',
            'content': server.users.keys()
            }
        if self.loggedIn == False:
            response['response'] = 'error'
            response['content'] = "You need to be loggin in to see names"
        # response["content"] = str(Server.users)
        if self.username:
            response['sender'] = self.username
        return response

    def help(self):
        helptext = """
        /login <username> - log in with the given username 
        /logout - log out
        <message> - send message
        /names - list users in chat
        /help - view help text
        """
        response = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'sender': '',
            'response': 'info',
            'content': helptext
            }

        if self.username:
            response['sender'] = self.username
        return response

    def history(self):
        response = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'sender': "",
        'response': 'history',
        'content': "\n".join(log)
        }
        if self.loggedIn == False:
            response['response'] = 'error'
            response['content'] = "You need to be loggin in to see names"
        # response["content"] = str(Server.users)
        if self.username:
            response['sender'] = self.username
        return response



    def send(self, data):
        if data["response"] == "message":
            for user in server.users:
                if user != self.username:
                    server.users[user].sendall(json.dumps(data))
        else:
            self.request.sendall(json.dumps(data))


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
    server.init()
    server.serve_forever()
