import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.10.96', 7890))

data = client.recv(1024).decode('utf-8')
print(data)

msg = input("Введите сообщение: ")
content = msg.encode('utf-8')
client.send(content)

data = client.recv(1024).decode('utf-8')
print(data)

client.shutdown(socket.SHUT_WR)