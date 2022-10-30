from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.clock import mainthread
from kivy.core.clipboard import Clipboard as Cb
import threading
import socket

KV = """
MyBL:
	orientation: "vertical"

	Label:
		font_size: "20sp"
		multiline: True
		text_size: self.width*0.98, None
		size_hint_x: 1.0
		size_hint_y: 0.6
		height: self.texture_size[1] 
		text: root.data_label
		markup: True
		on_ref_press: root.linki()		



	# TextInput:
	# 	id: Inp
	# 	font_size: "20sp"
	# 	multiline: False
	# 	padding_y: (5,5)
	# 	size_hint: (1, 0.1)
	# 	on_text: app.process()

    BoxLayout:
        Button:
            text: "Включить Розетку"
            bold: True
            background_color:'#00FFCE'
            size_hint: (0.5,0.15)
            on_press: root.onroz()
            
            
        Button:
            text: "Выключить Розетку"
            bold: True
            background_color:'#00FFCE'
            size_hint: (0.5,0.15)
            on_press: root.offroz()
		


	Button:
		text: "Start PC"
		bold: True
		background_color:'#00FFCE'
		size_hint: (1,0.15)
		on_press: root.startpc()

    Button:
		text: "Погода"
		bold: True
		background_color:'#00FFCE'
		size_hint: (1,0.15)
		on_press: root.pogoda()


	# Button:
	# 	text: "Отправить"
	# 	bold: True
	# 	background_color:'#00FFCE'
	# 	size_hint: (1,0.2)
	# 	on_press: root.callback3()

"""


class MyBL(BoxLayout):
    data_label = StringProperty("Подключение...")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # SERVER = "5.100.121.118"
        SERVER = "192.168.10.90"
        PORT = 7890

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        #self.client.sendall(bytes("979879789", 'UTF-8'))

        threading.Thread(target=self.get_data).start()

    def onroz(self):
        print("Запрос на включение отправлен!")
        self.client.sendall(bytes("startrozetka on", 'UTF-8'))

    def offroz(self):
        print("Запрос на выключение отправлен!")
        self.client.sendall(bytes("startrozetka off", 'UTF-8'))

    def startpc(self):
        print("Запуск ПК")
        self.client.sendall(bytes("startpc", 'UTF-8'))

    def pogoda(self):
        print("Запрос отправлен!")
        self.client.sendall(bytes("getwether", 'UTF-8'))


    # def callback3(self):
    #     print("Отправить")
    #     self.client.sendall(bytes(self.ids.Inp.text, 'UTF-8'))

    def get_data(self):
        while App.get_running_app().running:
            in_data = self.client.recv(4096)
            print("От сервера :", in_data.decode())
            kkk = in_data.decode()
            zzz = str(kkk)
            lines = zzz.split('\n')
            print(lines)
            if '\t\t\t\t\t' in lines:
                lines[4] = "==========="
            for ggg in lines:
                if ggg.startswith("https://"):
                    self.ttt = ggg

                    ggg = '[ref=linki][color=#00FFCE]' + ggg + '[/color][/ref]'
                self.set_data_label(ggg)

    def linki(self):
        print("В буффер")
        Cb.copy(self.ttt)

    @mainthread
    def set_data_label(self, data):
        self.data_label += str(data) + "\n"


class MyApp(App):
    running = True

    def process(self):
        text = self.root.ids.Inp.text

    def build(self):
        return Builder.load_string(KV)

    def on_stop(self):
        self.running = False


MyApp().run()
