from socket import AF_INET, socket, SOCK_STREAM
from _thread import *
import winsound
ENCODING = "iso 8859-1"
class Client:
    def __init__(self, address, name):
        self.socket_ = socket(AF_INET, SOCK_STREAM)
        self.name = name
        self.address = address
        start_new_thread(self.connect, ())

    def connect(self):
        try:
            self.socket_.connect(self.address)
            self.socket_.sendall(bytes(self.name, ENCODING))
            print("Connection Successful")
        except:
            print("Connection Failed")

        while True:
            try:
                data = self.socket_.recv(1024)
            except:
                print("User disconnected")
                break

    def send_msg(self, msg, encoding="iso 8859-1"):
        self.socket_.sendall(bytes(msg, encoding=encoding))
        #winsound.PlaySound("sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
