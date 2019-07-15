!/usr/bin/env python3

import socket
import sys

# The server's hostname or IP address
host = 'rtvm.cs.camosun.bc.ca'

# The port used by the server  
port = 80        

# The address of the webpages
resourse = "/ics226/lab1test1.html"

# create a socket called "s" in this format:
# s = socket.socket(addr_family, type)
# socket.AF_INET: Internet protocol (IPv4)
# socket.AF_INET6: Internet protocol (IPv6)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect((host, port))
s.sendall(b'Hello, world,I am sending a simple message to test my Python program')
data = s.recv(1024)

print('Received', repr(data))