# 装饰器模式

import socket


def respond(client):
    response = input("Enter a value: ")
    client.send(bytes(response, 'utf8'))
    client.close()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 2401))
server.listen(1)
try:
    while True:
        client, addr = server.accept()
        respond(client)
finally:
    server.close()


class LogSocket:
    def __init__(self, socket):
        self.socket = socket
    
    def send(self, data):
        print("Sending {0} to {1}".format(data, self.socket.getpeername()[0]))
        self.socket.send(data)
    
    def close(self):
        self.socket.close()


import gzip
from io import BytesIO


class GzipSocket:
    def __init__(self, socket):
        self.socket = socket
    
    def send(self, data):
        buf = BytesIO()
        zipfile = gzip.GzipFile(fileobj=buf, mode='w')
        zipfile.write(data)
        zipfile.close()
        self.socket.send(buf.getvalue())
    
    def close(self):
        self.socket.close()
    

import time


def log_calls(func):
    def wrapper(*args, **kwargs):
        now = time.time()
        print('Calling {0} with {1} and {2}'.format(func.__name__, args, kwargs))
        return_value = func(*args, **kwargs)
        print("Executed {0} in {1}ms".format(func.__name__, time.time() - now))
        return return_value
    return wrapper
    
