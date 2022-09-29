import os
from wakeonlan import send_magic_packet

def virtualboxstart():
    os.system('virtualbox')

def startpc():
    send_magic_packet('18:c0:4d:8e:c8:5a')