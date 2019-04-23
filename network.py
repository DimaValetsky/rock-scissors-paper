import socket
import pickle
from tkinter import Tk, Entry, Button, Label

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        root = Tk()

        def buttonClicked():
            global server
            global port
            port = int(b.get())
            server = a.get()
            root.destroy()

        a = Entry(root)
        a.place(relx=.2, rely=.1)
        b = Entry(root)
        b.place(relx=.2, rely=.3)
        Lip = Label(text="ip", fg="#eee", bg="#333")
        Lip.place(relx=.007, rely=.1)
        Lport = Label(text="port", fg="#eee", bg="#333")
        Lport.place(relx=.007, rely=.3)
        Bdimer = Button(root, width=7, command=buttonClicked, text="Connect")
        Bdimer.place(relx=.35, rely=.7)
        root.mainloop()
        self.addr = (server, port)
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

