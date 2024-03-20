import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 9999))
server_socket.listen(5)

while True:
    print('server is waiting for connections')
    client_socket, addr = server_socket.accept()
    print('connection from', addr)
    while True:
        data = client_socket.recv(1024)
        if not data or data.decode('utf-8') == 'END':
            break
        print('received from client', data.decode('utf-8'))
        try:
            client_socket.send(bytes('Hey there!', 'utf-8'))
        except:
            print('An error occurred!')
            break
    client_socket.close()