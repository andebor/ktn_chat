# -*- coding: utf-8 -*-
import socket
import json
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
        while True: #for testing
            self.handle_input()

        # TODO: Finish init process with necessary code

    def run(self):
        # Initiate the connection to the server
        self.connection.connect(('localhost', 9997))
        print "Connected to server 'localhost' with port 9997"

    def disconnect(self):
        self.connection.close()
        pass

    def receive_message(self, message):
    	#TEST_START
    	print "Message received: " + message
    	#TEST_SLUTT
        # TODO: Handle incoming message
        pass

    def send_payload(self, request, data):

        # Create json object
        data = {'request': request, 'content': data}

        # Convert json object to string
        message = json.dumps(data)

        # Send string
        self.connection.send(message)

        pass

    def handle_input(self):
        userinput = raw_input('Enter message: ')
        validated, error, requestType = self.validate_input(userinput)

        #Print error if not validated
        if validated == False:
            print error
            return
        
        if len(userinput.split()) > 1:
            message = userinput.split(' ', 1)[1]


        if requestType == 'login':
            self.username = userinput.split()[1].lower()
            self.send_payload('login', self.username)
        elif requestType == 'msg':
            self.send_payload('msg',message)
        elif requestType == 'names':
            self.send_payload('names', 'None')
        elif requestType == 'help':
            self.send_payload('help', 'None')
        elif requestType == 'logout':
            self.send_payload('logout', 'None')
        else:
            print "Unhandled error in user input"
            

    def validate_input(self, input):
        ok = True
        error = 'Invalid input: '
        

        #Check if at least two arguments
        if input.split() == [] :
            ok, error = False, error + "Missing arguments\n"

        #Get request type and message
        requestType = input.split()[0].lower()

        #Validate login
        if requestType == 'login':
            if self.loggedin == True:
                ok, error = False, error + "You are already logged in.\n"
            if len(input.split()) < 2:
                ok, error = False, error + "Please provide a username"

        if requestType == 'logout':
            if self.loggedin == False:
                ok, error = False, error + "You are already logged out."
        return ok, error, requestType


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
