from tkinter import *
from tkinter import ttk
from socket import AF_INET, socket, SOCK_STREAM, gethostbyname, gethostname
from Client import Client
from _thread import *
import winsound

BUFFER_SIZE = 1024
ENCODING = "iso 8859-1"
WIDTH = 54

class Chat_App(Frame):
    def __init__(self, parent, color, client_address, host_address, name):
        self.name = name
        self.parent = parent
        self.color = color
        self.parent['bg'] = self.color
        # Setting the client
        self.client = Client(client_address, name)

        # Setting the server
        self.socket_ = socket(AF_INET, SOCK_STREAM)
        self.address = host_address
        self.socket_.bind(host_address)
        start_new_thread(self.connect, ())
        self.user2 = "User 2:"
        self.first_time = True
        self.initGUI()

    def initGUI(self):
        Label(self.parent, text=self.name, font="Calibri 15 bold", fg='white', bg='deepskyblue4').pack(fill=X)
        self.chat_frame = Frame(self.parent, bg=self.color, height=460)
        self.chat_frame.pack(pady=5, fill=X, expand=1)
        self.chat_frame.pack_propagate(0)
        self.messages = Text(self.chat_frame, bg='white',font="Helvetica 12 bold", fg='blue', width=WIDTH)
        self.messages.config(state=DISABLED)
        self.messages.pack(side=LEFT, pady=5, padx=(5,0))
        scroll = ttk.Scrollbar(self.chat_frame)
        scroll.pack(side=LEFT, fill=Y, expand=NO)
        scroll.configure(command=self.messages.yview)
        self.messages.configure(yscrollcommand=scroll.set)

        self.entry_frame = Frame(self.parent, bg=self.color)
        self.entry_frame.pack(pady=5, fill=X, expand=1)
        self.entrybox = Entry(self.entry_frame, font="System 14 bold")
        self.entrybox.pack(side= LEFT,pady=5,padx=5, fill = X, expand =1)
        self.entrybox.focus_set()
        self.entrybox.bind("<Return>", self.chat)
        send = ttk.Button(self.entry_frame, text = "Send", width=20,command= self.chat)
        send.pack(side = RIGHT,pady=15,padx=15)

    def chat(self, event=0):
        message = self.entrybox.get()
        if len(message)>0:
            try:
                self.client.send_msg(message)
                self.messages.config(state=NORMAL)
                self.messages.insert(END, self.name+": " + message+"\n")
                line_number = float(self.messages.index('end')) - 1.0
                self.messages.tag_add("user1", line_number, line_number + 0.4)
                self.messages.tag_config("user1", foreground="#04cc14", font=("Arial", 12, "bold"), justify=LEFT)
                self.messages.see(END)
                self.entrybox.delete(0,END)
                self.messages.config(state=DISABLED)
            except OSError as e:
                print("Message could not be sent")
                print(str(e))

    def connect(self):
        self.socket_.listen(5)
        connection, address = self.socket_.accept()
        print("%s connected" % (str(address)))
        if self.first_time:
            data = connection.recv(1024)
            self.user2 = data.decode(ENCODING)
            self.first_time = False
        while True:
            try:
                data = connection.recv(1024)
                msg = self.user2+": " + data.decode(ENCODING)
                self.messages.config(state=NORMAL)
                self.messages.insert(END, msg)
                line_number = float(self.messages.index('end')) - 1.0
                self.messages.tag_add("user2", line_number, line_number + 0.6)
                self.messages.tag_config("user2", foreground="#c10707", font=("Arial", 12, "bold"), justify=RIGHT)
                winsound.PlaySound("sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
                self.messages.insert(END, '\n')
                self.messages.config(state=DISABLED)
            except:
                self.connect()
                break
        connection.close()


if __name__ == '__main__':
    root = Tk()
    s = socket(AF_INET, SOCK_STREAM)
    #CLIENT_ADDRESS = ("10.50.80.64", 33000)  ## add client address here
    CLIENT_ADDRESS = (gethostbyname(gethostname()), 33000)  ## add client address here
    HOST_ADDRESS = (gethostbyname(gethostname()), 33000)  ## add host(local) address here
    o = Chat_App(root, 'honeydew', CLIENT_ADDRESS, HOST_ADDRESS, "Abdul Jaleel")

    root.geometry(str(WIDTH*10)+'x600+700+30')
    root.mainloop()
