#!/usr/bin/python3
import os
import socket, threading
from wakeonlan import send_magic_packet
import yaml
import sys
import logging

# Блок функций исполняющих действия

def startpc():
    send_magic_packet('18:c0:4d:8e:c8:5a')

def restartapache():
    os.system('systemctl restart apache2')


# Жизненый цикл подключения
class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        logging.info("Новое подключение: ", clientAddress)

    def run(self):
        logging.info("Подключение с клиента : ", clientAddress)
        self.csocket.send(bytes('Добро пожаловать на сервер romanhand.ru', 'UTF-8'))
        msg = ''
        while True:
            data = self.csocket.recv(4096)
            msg = data.decode()
            logging.info(msg)

            if msg == '':
                logging.info("Отключение")
                break

            elif msg == 'startpc':
                self.csocket.send(bytes('Магический пакет отправлен!', 'UTF-8'))
                startpc()
            elif msg == 'restartapache':
                self.csocket.send(bytes('Apache2 перезапущен!', 'UTF-8'))
                startpc()
            else:
                self.csocket.send(bytes('Команда не найдена:(', 'UTF-8'))

            logging.info("Запрос " + str(msg) + " обработан")

        logging.info("Клиент ", clientAddress, " покинул нас...")

def debugArg():
    try:
        debug = (sys.argv[1])
        if len(sys.argv) > 1:
            if debug == "-d" or debug == "--debug":
                debug = True
        else: debug = False
    except: debug = False
    return debug


if __name__ == "__main__":



    # Проверка на аргумент -d --debug для сбора доп логов
    debug = debugArg()


    # Обьявляем логи
    if debug:srclog = "rcs.log"
    else: srclog = "/var/log/rcs.log"

    logging.basicConfig(filename="rcs.log")


    # Читаем конфиг
    if debug: srcyaml = 'remotecontrol.yaml'
    else: srcyaml = '/etc/rcs/remotecontrol.yaml'


    # Назначение переменных из конфига
    try:
        with open(srcyaml, "r") as fh:
            configs = yaml.safe_load(fh)
        HOST = configs['host']
        PORT = configs['port']
        USERNAME = configs['username']
    except: logging.error("Проблема с конфигом!")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))

    print("Сервер запущен, " + USERNAME + "!")

    while True:
        server.listen(1)
        clientsock, clientAddress = server.accept()
        newthread = ClientThread(clientAddress, clientsock)
        newthread.start()

