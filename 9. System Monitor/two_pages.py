#Written with Python 3.6
from tkinter import *
import tkinter as tk
import platform, socket, psutil
from threading import Thread
from tkinter import ttk
from tkinter import messagebox
from time import sleep


LARGE_FONT = "Verdana 12"  # font's family is Verdana, font's size is 12
global data
data = ''

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title('System Monitor')  # set the title of the main window
        self.geometry('920x520+270+30')  # set size of the main window to 300x300 pixels
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
        label = tk.Label(self, text='Add Device', font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        button1 = tk.Button(self, text='See All Devices', font = LARGE_FONT , command=lambda: controller.show_frame(PageOne))
        button1.pack()

        Label(self, text='IP Address', font = LARGE_FONT).pack(side=LEFT, pady=5, anchor = N, padx=5)
        self.entry = Entry(self, width=55, font=" 12")
        self.entry.pack(side=LEFT, anchor = N, pady=5, padx=5)
        self.entry.insert(END, '192.168.72.128')
        Button(self, text='Add', width=20, command=self.addDevice).pack(side=LEFT, anchor = N, pady=5, padx=5)

    def addDevice(self):
        ip_ad = self.entry.get()
        try:
            #if int(ip_ad.replace('.', '')):
                #tkMessageBox.showwarning('No client found', 'Add and choose client')
            thread = Thread(target=self.connect2device, args=(ip_ad,))
            thread.start()
            #self.connect2device(ip_ad)

        except ValueError:
            messagebox.showwarning('Error!', 'Wrong IP Address')

    def connect2device(self, ipAddress):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 8888
        s.connect((ipAddress, port))
        global data
        while True:
            data = str(s.recv(1024).decode('utf-8'))

            sleep(3)

        #s.close()



class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text='All Devices', font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        tk.Button(self, text='Add Device', font = LARGE_FONT, command=lambda: controller.show_frame(StartPage)).pack(pady=5)
        self.initGUI()

    def initGUI(self):
        self.main_frame = Frame(self)
        self.main_frame.pack(fill=BOTH, expand=1)
        self.frame = Frame(self.main_frame, highlightbackground="blue", highlightthickness=1,highlightcolor="blue",bd=0)
        self.frame.pack(fill=BOTH, expand=1)
        self.frame.pack_propagate(0)
        self.south_frame = Frame(self.main_frame, highlightbackground="blue", highlightthickness=1,highlightcolor="blue",bd=0)
        self.south_frame.pack(fill=BOTH, expand=1)
        self.south_frame.pack_propagate(0)
        #Left Side
        self.frame1 = Frame(self.frame)
        self.frame1.pack(pady=5,padx=5, fill=BOTH, expand=1, side=LEFT)
        self.frame1.pack_propagate(0)

        self.title = Label(self.frame1,font="Calibri 20 bold", text="Status", bg='blue', fg= 'white')
        self.title.pack(pady=3, fill=X, expand=0, side = TOP)

        self.allClients = Label(self.frame1, font="Calibri 15 bold")
        self.allClients.pack(pady=5, anchor=W)
        self.onlineClients = Label(self.frame1, font="Calibri 15 bold")
        self.onlineClients.pack(pady=5, anchor=W)
        self.offlineClients = Label(self.frame1, font="Calibri 15 bold")
        self.offlineClients.pack(pady=5, anchor=W)

        #Right side
        self.frame2 = Frame(self.frame, highlightbackground="blue", highlightthickness=1,highlightcolor="blue",bd=0 , height=300)
        self.frame2.pack(fill=BOTH, expand=1, side=LEFT,anchor=NW)

        self.tree = ttk.Treeview(self.frame2)

        self.tree["columns"] = ('1', '2', '3')
        self.tree.column('#0', width=100, anchor='center')
        self.tree.column('1', width=100, anchor = 'center')
        self.tree.column('2', width=100, anchor = 'center')
        self.tree.column('3', width=100, anchor = 'center')
        self.tree.heading("#0", text="Device")
        self.tree.heading('1', text="CPU")
        self.tree.heading('2', text="RAM")
        self.tree.heading('3', text="HDD")
        self.tree.insert('', 'end', 'host', text='Host', values = ('0','0','0'), tags=('row1'))
        self.tree.tag_bind('row1', '<1>', self.showClientDetails)
        self.tree.pack(fill=BOTH, expand=True)

        self.frame2.pack_propagate(0)

        #South Frame
        self.frame3 = Frame(self.south_frame)
        self.frame3.pack(pady=5, padx=5, fill=BOTH, expand=1)
        self.frame3.pack_propagate(0)

        self.clientName = Label(self.frame3, font="Calibri 15 bold", text="Name         : ")
        self.clientName.pack(pady=5, anchor=W)
        self.clientIP = Label(self.frame3, font="Calibri 15 bold", text="IP Address : ")
        self.clientIP.pack(pady=5, anchor=W)
        self.clientPlatform = Label(self.frame3, font="Calibri 15 bold", text="Platform    : ")
        self.clientPlatform.pack(pady=5, anchor=W)
        self.clientProcessor = Label(self.frame3, font="Calibri 15 bold", text="Processor  : ")
        self.clientProcessor.pack(pady=5, anchor=W)

        self.first = True
        self.updateInfo()

    def cpu_update(self):
        #PC1:
        #while True:
        cpu_usage = str(psutil.cpu_percent(1))
        ram_usage = str(psutil.virtual_memory().percent)
        hdd_usage = str(psutil.disk_usage('C:\\').percent)

        self.tree.item('host', values=(cpu_usage, ram_usage, hdd_usage))
        threshold = 20
        if float(cpu_usage) > threshold:
            self.tree.tag_configure('row1', background = 'red')
        else:
            self.tree.tag_configure('row1', background='')

        # PC2:
        global data

        if len(data) > 0:
            val1, val2, val3 = data.split(',')
            if self.first == True:
                self.tree.insert('', 'end', 'vm', text='VM', values=(val1, val2, val3), tags=('row2'))
                self.first = False
            else:
                self.tree.item('vm', values=(val1, val2, val3))

        self.after(10000,self.cpu_update)

    def updateInfo(self):
        self.allClients.config(text="Total Devices          : 2")
        self.onlineClients.config(text="Online                    : 1" )
        self.offlineClients.config(text="Offline                    : 1")

        self.cpu_update()

    def showClientDetails(self, event=None):
        name = platform.node()
        ipAd = socket.gethostbyname(socket.gethostname())
        systemOS = platform.platform()
        processor = platform.processor().split(' ')[0]
        self.clientName.config(text="Name         : " + name)
        self.clientIP.config(text="IP Address : " + ipAd)
        self.clientPlatform.config(text="Platform    : " + systemOS)
        self.clientProcessor.config(text="Processor  : " + processor)

        #tkMessageBox.showwarning('No client found', 'Add and choose client')


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()