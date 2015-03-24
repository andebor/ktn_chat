# -*- coding: utf-8 -*-
from threading import Thread

class MessageReceiver(Thread):
    """
    This is the message receiver class. The class inherits Thread, something that
    is necessary to make the MessageReceiver start a new thread, and permits
    the chat client to both send and receive messages at the same time
    """

    BUFFER_SIZE = 1024

    def __init__(self, client, connection):
        """
        This method is executed when creating a new MessageReceiver object
        """
        Thread.__init__(self)

        # Flag to run thread as a deamon
        self.daemon = True

        # TODO: Finish initialization of MessageReceiver
        self.client = client
        self.connection = connection
        Thread.start(self)

    def run(self):
        # TODO: Make MessageReceiver receive and handle payloads
        connection.listen(True)    #lytt til server
        print "Listening for messages ...\n"
        while True:
            try:
                message = connection.recv(BUFFER_SIZE)
            except IOError:
                print "Could not receive message from server"
                message = "Placeholder"
            #sove litt?
            #message = "Placeholder" #Melding mottatt fra server
            self.client.receive_message(message)
            break