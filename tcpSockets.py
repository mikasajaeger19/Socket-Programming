from socket import *
import socket
import sys

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error as err:
    print("Failed to create a socket:" + str(err))
    sys.exit()
print("socket created")

target_host = input("Enter the target_hostname to connect: ")
target_port = (input("Enter the target_port to connect: "))

try:
    sock.connect((target_host, int(target_port)))
    print("socket connected to: " + target_host + " on port " + target_port)
    sock.shutdown(2)
except socket.error as err:
    print("Failed to connect to socket:" + str(err))
    sys.exit()
