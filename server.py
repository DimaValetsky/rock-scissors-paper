import socket
from _thread import *
import pickle
from game import Game
from tkinter import Tk, Entry, Button, Label

server = "127.0.0.1"
port = 5555

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
Bdimer = Button(root, width=7, command=buttonClicked, text = "Connect")
Bdimer.place(relx=.35, rely=.7)
root.mainloop()

print(server,port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()
                    elif data != "get":
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print("Lost connection")
    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:
        games[gameId].ready = True
        p = 1

    start_new_thread(threaded_client, (conn, p, gameId))
