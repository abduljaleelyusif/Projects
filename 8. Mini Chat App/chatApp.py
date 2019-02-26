from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from socket import *
from threading import Thread
from Client import Client
from _thread import *
from tkinter.scrolledtext import ScrolledText
import winsound
name = 'AJ'
user2 = 'VM'

COLOR = 'turquoise3'
LARGE_FONT = "Verdana 12"  # font's family is Verdana, font's size is 12

HOST = '10.50.94.178'
#HOST = ''
PORT = 53750
BUFFER_SIZE = 1024
ENCODING = "utf-8"
ADDR = (HOST, PORT)
PROTOCOL = 1



emojis = {'☪': '?0?', '❤': '?1?', '\ud83d\ude00': '?2?', '\ud83d\ude01': '?3?', '\ud83d\ude02': '?4?', '\ud83e\udd23': '?5?', '\ud83d\ude03': '?6?', '\ud83d\ude04': '?7?', '\ud83d\ude05': '?8?', '\ud83d\ude06': '?9?', '\ud83d\ude09': '?10?', '\ud83d\ude0a': '?11?', '\ud83d\ude0b': '?12?', '\ud83d\ude0e': '?13?', '\ud83d\ude0d': '?14?', '\ud83d\ude18': '?15?', '\ud83d\ude17': '?16?', '\ud83e\udd17': '?17?', '\ud83e\udd14': '?18?', '\ud83d\ude10': '?19?', '\ud83d\ude44': '?20?', '\ud83d\ude0f': '?21?', '\ud83d\ude2e': '?22?', '\ud83e\udd10': '?23?', '\ud83d\ude34': '?24?', '\ud83d\ude0c': '?25?', '\ud83d\ude1c': '?26?', '\ud83d\ude14': '?27?', '\ud83d\ude15': '?28?', '\ud83d\ude32': '?29?'}



class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('Chat App')  # set the title of the main window
        self.geometry('800x600+170+30')  # set size of the main window to 300x300 pixels
        #self.state("zoomed")

        # this container contains all the pages
        container = tk.Frame(self)
        container.pack(side='top', fill ='both', expand = True)
        container.grid_rowconfigure(0, weight=1)  # make the cell in grid cover the entire window
        container.grid_columnconfigure(0, weight=1)  # make the cell in grid cover the entire window
        self.frames = {}  # these are pages we want to navigate to

        for F in (StartPage, PageOne):  # for each page
            frame = F(container, self)  # create the page
            self.frames[F] = frame  # store into frames
            frame.grid(row=0, column=0, sticky='nsew')  # grid it to container

            self.show_frame(StartPage)  # let the first page is StartPage

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        frame = Frame(self)
        frame.pack(anchor = N, fill=BOTH, expand=1)

        frame0 = Frame(frame)
        frame0.pack(fill=X, expand=0)
        label = tk.Label(frame0, text='Project 1', font='Verdana 24', fg = 'blue')
        label.pack(pady=10, padx=10)

        frame1 = Frame(frame)
        frame1.pack(fill=X, expand=0)
        frame2 = Frame(frame)
        frame2.pack(fill=X, expand=0)
        frame3 = Frame(frame)
        frame3.pack(fill=X, expand=0)

        Label(frame1, text='Enter Destination IP: ', font = LARGE_FONT).pack(side=LEFT, pady=5, anchor = N, padx=5)
        self.entry = Entry(frame1, width=55, font=" 12")
        self.entry.pack(side=LEFT, anchor = N, pady=5, padx=5)
        self.entry.insert(END, HOST)

        Label(frame2, text='Protocol: ', font=LARGE_FONT).pack(side= LEFT, pady=5, anchor=N, padx=5)
        self.v = IntVar()
        self.v.set(PROTOCOL)
        tcp = ttk.Radiobutton(frame2,text="TCP", variable=self.v,value= 1,command = lambda : self.getProtocol(tcp))
        tcp.pack(side = LEFT, anchor = N, padx=110, pady=5,)
        udp = ttk.Radiobutton(frame2, text="UDP", variable=self.v, value= 2, command = lambda : self.getProtocol(udp))
        udp.pack(side=LEFT, anchor=N, padx=110, pady=5,)


        tk.Button(frame3, text='Start Connection =>', font=LARGE_FONT,
                            command=lambda: controller.show_frame(PageOne)).pack(anchor=N)
        Label(frame3, text='Waiting to Connect to Partner... ', font=LARGE_FONT, fg = 'red').pack(pady=10, anchor=N, padx=5)

    def getProtocol(self, widget):
        if widget['text'] == 'TCP':
            PROTOCOL = 1
        else:
            PROTOCOL = 2

class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.line = 1.0
        self.initGUI()

        if PROTOCOL == 1:  # TCP
            self.client_socket = socket(AF_INET, SOCK_STREAM)
            self.client_socket.connect(ADDR)
        else:  # UDP
            self.client_socket = socket(AF_INET, SOCK_DGRAM)
            self.client_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)  # Make Socket Reusable
            # self.client_socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)  # Allow incoming broadcasts
            # self.client_socket.setblocking(False)  # Set socket to non-blocking mode
            self.client_socket.bind(('',PORT))


        receive_thread = Thread(target=self.receive)
        receive_thread.start()

    def initGUI(self):
        main_frame = Frame(self)
        main_frame.pack(fill=BOTH, expand=1)

        self.frame = Frame(main_frame, bg = COLOR)
        self.frame.pack(fill=BOTH, expand=1)
        #self.frame.pack_propagate(0)
        Label(self.frame, text= name, font=LARGE_FONT, fg='white', bg=COLOR).pack(fill=X)
        self.chat_frame = Frame(self.frame, bg= 'white', width=780)
        self.chat_frame.pack(pady=10,padx=10, fill=BOTH, expand=0)
        #self.chat_frame.pack_propagate(0)
        self.messages = ScrolledText(self.chat_frame, bg='white',font="Verdana 13", fg='blue')
        self.messages.config(state=DISABLED)
        self.messages.pack(side=LEFT, pady=5, padx=5, fill=BOTH, expand = 1)

        self.entry_frame = Frame(self.frame, bg=COLOR, height=50)
        self.entry_frame.pack(pady=5,padx=5, fill=X, expand=1)
        self.entrybox = Text(self.entry_frame, font="Verdana 18", width=34, bd=2)
        self.entrybox.pack(side= LEFT,pady=5,padx=5, fill = BOTH, expand =1)
        self.entrybox.focus_set()
        self.entrybox.bind("<Return>", self.chat)



        Button(self.entry_frame, text = "   Send   ", font=LARGE_FONT, command= self.chat).pack(side = RIGHT,pady=5,padx=5, fill=BOTH, expand=0)
        #Button(self.entry_frame, text= u'\uD83D\uDE03' , font='28',command=lambda: self.controller.show_frame(StartPage)).pack(pady=15,padx=15)
        Button(self.entry_frame, text=u'   \uD83D\uDE03   ', font='32',command = self.create_emojis).pack(side = RIGHT, pady=5, padx=5,fill=BOTH, expand=0)



    def create_emojis(self):
        top = Toplevel()
        top.title('Emojis')
        top.geometry('390x128+540+420')
        self.ebutton = []
        for i, icon in enumerate(emojis.keys()):
            self.ebutton.append(Button(top, text=icon, font='24', fg='red', command=self.insert_emoji(icon)))
            row, col = divmod(i, 10)
            self.ebutton[i].grid(sticky=W + E + N + S, row=row, column=col, padx=1, pady=1)

    def insert_emoji(self, emoticon):  # This is the callback factory. Calling it returns a function.
        def _ie():
            msg = self.entrybox.get('1.0', END).replace('\n', "")
            self.entrybox.delete('1.0',END)
            msg += emoticon
            self.entrybox.insert('1.0', msg)

        return _ie

    def chat(self, event=None):
        message = self.entrybox.get('1.0',END)
        if len(message)>0 and not message.isspace():
            try:
                if PROTOCOL == 1: #TCP
                    try:
                        self.client_socket.send(bytes(message, ENCODING))
                    except UnicodeEncodeError:
                        self.client_socket.send(bytes(emojis[message.strip()], ENCODING))
                else: #UDP
                    try:
                        self.client_socket.sendto(bytes(message, ENCODING),self.addr)
                    except UnicodeEncodeError:
                        self.client_socket.sendto(bytes(emojis[message.strip()], ENCODING),self.addr)
                    except AttributeError:
                        #self.udpdata, self.addr = self.client_socket.recvfrom(BUFFER_SIZE)
                        self.addr = ADDR
                        self.client_socket.sendto(bytes(message, ENCODING), self.addr)
                self.messages.config(state=NORMAL)
                self.messages.insert(END, name + ": " + message.strip() + "\n")
                line_number = self.line + ((len(name)+1)/10.0)
                self.messages.tag_config('user1', foreground='red')
                self.messages.tag_add("user1", self.line, line_number)
                self.line += 1.0
                self.messages.see(END)
                self.entrybox.delete('1.0',END)
                self.messages.config(state=DISABLED)
                return 'break'
            except OSError as e:
                print("Message could not be sent")
                print(str(e))
                return 'break'




    def receive(self):
        while True:
            try:
                if PROTOCOL == 1: #TCP
                    data = self.client_socket.recv(BUFFER_SIZE).decode(ENCODING)
                else:
                    self.udpdata, self.addr = self.client_socket.recvfrom(BUFFER_SIZE)
                    data = self.udpdata.decode(ENCODING)
                if len(data):
                    if data.strip()[0] == '?' and data.strip()[-1] == '?':
                        data = [icon for icon in emojis.keys() if emojis[icon] == data.strip()][0]
                        msg = user2 + ": " + data
                    else:
                        msg = user2 + ": " + data
                    self.messages.config(state=NORMAL)
                    self.messages.insert(END, msg.strip() + '\n')
                    line_number = self.line + ((len(user2) + 1) / 10.0)
                    self.messages.tag_config('userTwo', foreground='green')
                    self.messages.tag_add("userTwo", self.line, line_number)
                    self.line += 1.0
                    winsound.PlaySound("sound.wav", winsound.SND_ASYNC | winsound.SND_ALIAS)
                    self.messages.config(state=DISABLED)
            except OSError:  # Possibly client has left the chat.
                print("Your partner left")
                break
            except AttributeError:
                break
        #self.client_socket.close()

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()