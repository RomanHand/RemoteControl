import socket, threading
import commands



class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("Новое подключение: ", clientAddress)

    def run(self):
        print("Подключение с клиента : ", clientAddress)
        self.csocket.send(bytes('Добро пожаловать на сервер romanhand.ru', 'UTF-8'))
        msg = ''
        while True:
            data = self.csocket.recv(4096)
            msg = data.decode()
            print(msg)

            if msg == '':
                print("Отключение")
                break

            elif msg == 'virtualbox':
                self.csocket.send(bytes('virtualbox запущен!', 'UTF-8'))
                commands.virtualboxstart()
            elif msg == 'startpc':
                self.csocket.send(bytes('Магический пакет отправлен!', 'UTF-8'))
                commands.startpc()
            else:
                self.csocket.send(bytes('Команда не найдена:(', 'UTF-8'))


            #elif msg == 'Поиск по названию':
            #    f = open("text.txt", "w")
            #    f.write("название")
            #    f.close()
            #    self.csocket.send(bytes('Введите название:', 'UTF-8'))

            print("Запрос " + str(msg) + " обработан")

        print("Клиент ", clientAddress, " покинул нас...")

HOST = "192.168.10.96"
PORT = 7890

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
print("Сервер запущен!")

while True:
    server.listen(1)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()