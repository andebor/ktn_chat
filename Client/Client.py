# -*- coding: utf-8 -*-
import socket
import json
import time
from MessageReceiver import *

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        # Set up the socket connection to the server
        self.host = host
        self.server_port = server_port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.loggedin = False
        self.run()
        self.messagereceiver = MessageReceiver(self, self.connection)
        #self.messagereceiver.__init__()
        #self.messagereceiver.start()
        self.terminate = False
        while self.terminate == False: #for testing
            # self.testing()
            self.handle_input()

        self.disconnect()
        # TODO: Finish init process with necessary code

    def run(self):
        # Initiate the connection to the server
        self.connection.connect(('localhost', 9997))
        print "Connected to server 'localhost' with port 9997"

    def disconnect(self):
        self.connection.close()

    def receive_message(self, message):
    	#TEST_START
    	# print "Message received"

        data = json.loads(message)
        print '\n'

        if data["response"] == "info":
            print str(data["content"])
        elif data["response"] == "error":
            print str(data["content"])
        elif data["response"] == "message":
            print data["sender"] + ": " + data["content"]

    	#TEST_SLUTT
        # TODO: Handle incoming message


    def send_payload(self, request, content):

        # Create json object
        data = {'request': request, 'content': content}

        # Convert json object to string
        message = json.dumps(data)

        # Send string
        self.connection.send(message)

        # print "Message sent: " + str(data)  #for testing



    def testing(self):
        request = raw_input('Enter request: ')
        content = raw_input('Enter content: ')
        self.send_payload(request, content)


    def handle_input(self):
        time.sleep(0.1)
        userinput = raw_input('--> ')
        validated, error, requestType = self.validate_input(userinput)

        #Print error if not validated
        if validated == False:
            print error
            return
        
        if requestType == '/login':
            self.username = userinput.split()[1].lower()
            self.send_payload('login', self.username)
            self.loggedin = True
        elif requestType == '/names':
            self.send_payload('names', 'None')
        elif requestType == '/help':
            self.send_payload('help', None)
        elif requestType == '/logout':
            self.logout()
        # elif requestType == '/exit':
        #     if self.loggedin == True:
        #         self.logout()
        #     self.terminate = True
        else:
            self.send_payload('msg',userinput)

            
    def logout(self):
        self.send_payload('logout', None)
        self.loggedin = False

    def validate_input(self, input):
        ok = True
        error = 'Invalid input: '
        requestType = None
        

        #Check if at least two arguments
        if input.split() == [] :
            ok, error = False, error + "Missing arguments\n"
        else:
            #Get request type and message
            requestType = input.split()[0].lower()

            #Validate login
            if requestType == '/login':
                if self.loggedin == True:
                    ok, error = False, error + "You are already logged in.\n"
                if len(input.split()) < 2:
                    ok, error = False, error + "Please provide a username\n"

            if requestType == '/logout':
                if self.loggedin == False:
                    ok, error = False, error + "You are already logged out.\n"

            # if requestType == 'msg':
            #     if len(input.split()) < 2:
            #         ok, error = False, error + "Please provide a message\n"
        return ok, error, requestType


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
