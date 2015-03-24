# -*- coding: utf-8 -*-
import socket
import json

class Client:
    """
    This is the chat client class
    """

    def __init__(self, host, server_port):
        """
        This method is run when creating a new Client object
        """
        # Set up the socket connection to the server
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

        # TODO: Finish init process with necessary code

    def run(self):
        # Initiate the connection to the server
        self.connection.connect(('localhost', 9997))
        print "Connected to server 'localhost' with port 9997"

    def disconnect(self):
        self.connection.close()
        pass

    def receive_message(self, message):
        # TODO: Handle incoming message
        pass

    def send_payload(self, data):

        # Create json object
        data = {'request': 'message', 'message': data}

        # Convert json object to string
        message = data = json.dumps(data)

        # Send string
        self.send(message)


        pass


if __name__ == '__main__':
    """
    This is the main method and is executed when you type "python Client.py"
    in your terminal.

    No alterations is necessary
    """
    client = Client('localhost', 9998)
