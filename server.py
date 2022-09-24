import socket


def startserver():
    global server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('192.168.10.96', 1488))
        server.listen(100)
        while True:
            print('Wait...')
            client_socket, address = server.accept()
            data = client_socket.recv(1024).decode('utf-8')
            print(data)
            content = 'Done'.encode('utf-8')
            client_socket.send(content)
            client_socket.shutdown(socket.SHUT_WR)
            if data == "1":
                print("!@3")
    except KeyboardInterrupt:
        server.close()


if __name__ == '__main__':
    startserver()
