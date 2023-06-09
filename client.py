import socket
import threading
import tkinter
from tkinter import *
from tkinter import simpledialog


class Chat:

    def __init__(self):

        HOST = '127.0.0.1'
        PORT = 55555

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))

        # Interface
        login = Tk()
        login.withdraw()
        self.window_loading = False
        self.ativo = True

        # Inputs
        self.nome = simpledialog.askstring('Name', 'Enter your name!', parent=login)
        self.classs = simpledialog.askstring('Class', 'Enter your class!', parent=login)
        
        thread = threading.Thread(target=self.connect)
        thread.start()
        self.window()

    def window(self):
        self.root = Tk()
        self.root.geometry('800x800')
        self.root.title('Chat')

        self.box_text = Text(self.root)
        self.box_text.place(relx=0.05, rely=0.01, width=700, height=600)

        self.send_message = Entry(self.root)
        self.send_message.place(relx=0.05, rely=0.8, width=500, height=20)

        self.btn_send = Button(self.root, text='Send', command=self.sendMessage)
        self.btn_send.place(relx=0.7, rely=0.8, width=100, height=20)
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.root.mainloop()

    def close(self):
        self.root.destroy()
        self.client.close()

    def connect(self):
        while True:
            received = self.client.recv(1024)
            if received == b'SALA':
                self.client.send(self.classs.encode())
                self.client.send(self.nome.encode())
            else:
                try:
                    self.box_text.insert('end', received.decode())
                except:
                    pass


    def sendMessage(self):
        message = self.send_message.get()
        self.client.send(message.encode())


chat = Chat()