import threading
import socket

host = '192.168.1.4'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
aliases = []

def sendMessage(message, senderClient):
    for client in clients:
        if client != senderClient:
            client.send(message)

def broadcast(message):
    for client in clients:
        client.send(message)

def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            sendMessage(message, client)
        except:
            index = clients.index(client)
            alias = aliases[index]
            broadcast(f'{alias} has left the chat!'.encode('utf-8'))
            clients.remove(client)
            client.close()
            aliases.remove(alias)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('alias? '.encode('utf-8'))
        alias = client.recv(1024)
        aliases.append(alias)
        clients.append(client)

        print(f'Alias of the client is {alias}'.encode('utf-8'))
        broadcast(f'{alias} has connected to the chat!'.encode('utf-8'))
        client.send('Connected to the server!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()