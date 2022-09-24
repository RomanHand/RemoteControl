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
	size_hint: (0.95, 0.95)
	pos_hint: {"center_x": 0.5, "center_y":0.5}

	Label:
		font_size: "15sp"
		multiline: True
		text_size: self.width*0.98, None
		size_hint_x: 1.0
		size_hint_y: None
		height: self.texture_size[1] + 15
		text: root.data_label
		markup: True
		on_ref_press: root.linki()		



	TextInput:
		id: Inp
		multiline: False
		padding_y: (5,5)
		size_hint: (1, 0.5)
		on_text: app.process()
		

	Button:
		text: "Virtualbox"
		bold: True
		background_color:'#00FFCE'
		size_hint: (1,0.5)
		on_press: root.callback2()

	Button:
		text: "Случайный"
		bold: True
		background_color:'#00FFCE'
		size_hint: (1,0.5)
		on_press: root.callback3()

	Button:
		text: "Отправить"
		bold: True
		background_color:'#00FFCE'
		size_hint: (1,0.5)
		on_press: root.callback4()

"""


class MyBL(BoxLayout):
    data_label = StringProperty("Подключение...")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        SERVER = "192.168.10.96"
        PORT = 1488

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        self.client.sendall(bytes("979879789", 'UTF-8'))

        threading.Thread(target=self.get_data).start()

    def callback2(self):
        print("Запуск Virtualbox")
        self.client.sendall(bytes("virtualbox", 'UTF-8'))

    def callback3(self):
        print("Случайный")
        self.client.sendall(bytes("Случайный", 'UTF-8'))

    def callback4(self):
        print("Отправить")
        self.client.sendall(bytes(self.ids.Inp.text, 'UTF-8'))

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
