# -*- coding: utf-8 -*-

import socket
import json


class Server_Handler():

    def __init__(self):
        # creating the socket and chosing TCP connection.
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_ip = '127.0.0.1'  # defult server ip.
        self.server_port = 5000  # defult server port.

        self.data = []  # this will be used as an que from reseved data.
        self.connected = False

        # Creating all the defults for an server / listener.
    def server(self, ip):
        self.connection = None
        self.client_address = None
        if ip:
            self.server_ip = ip

        # This is used to prevent the "Address ocepyed error"
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # Binding the address to the socket.
        self.sock.bind((self.server_ip, self.server_port))
        self.sock.listen(1)

        # Opens the connection and redeclaring "self.sock".
        self.sock, self.client_address = self.sock.accept()

        # Creating all the defults for an client / connecter.
    def clinet(self, ip, msg):
        server_address = (ip, self.server_port)
        self.sock.connect(server_address)
        self.send(msg)
        self.connected = True

        # Listens for incomming messages.
    def listen(self):
        while True:
            data = self.sock.recv(2048)
            if data:
                if self.connected == False:
                    self.connected = True
                self.data = data
                break

        # Sending messages
    def send(self, msg):
        self.sock.sendall(msg)

        # Do not forget to close your connection
    def close(self):
        if self.connected == True:
            self.connected = False
        self.sock.close()


class Messages():

    def encode(self, j):
        return json.dumps(j)

    def decode(self, msg):
        return json.loads(msg)
