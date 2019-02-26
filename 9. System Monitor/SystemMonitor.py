#Real time plotting code was retrieved from: https://stackoverflow.com/questions/15736393/live-plot-in-python-gui
#Written with Python 2.7
from Tkinter import *
import Tkinter as tk
import psutil, ctypes, winsound

user32 = ctypes.windll.user32
screenWidth = user32.GetSystemMetrics(0)


class monitorPage(Frame):

    def __init__(self, parent, color):
        Frame.__init__(self)
        self.parent = parent
        self.color = color
        self.parent['bg'] = self.color
        self.initGUI()

    def initGUI(self):

        self.frame1 = Frame(self.parent, bg=self.color)
        self.frame1.pack(pady=5, fill=BOTH, expand=1)
        self.frame1.pack_propagate(0)
        self.cpuState = Label(self.frame1, text='CPU', font="Calibri 15 bold", fg='white', bg='red')
        self.cpuState.pack(fill=X)

        self.canvas1 = Canvas(self.frame1)
        self.canvas1.pack(fill=X, expand=1)


        #################
        self.frame2 = Frame(self.parent, bg=self.color)
        self.frame2.pack(pady=5, fill=BOTH, expand=1)
        self.frame2.pack_propagate(0)
        self.memState = Label(self.frame2, text='Memory', font="Calibri 15 bold", fg='white', bg='red')
        self.memState.pack(fill=X)
        self.canvas2 = Canvas(self.frame2)
        self.canvas2.pack(fill=X, expand=1)


        #################
        self.frame3 = Frame(self.parent, bg=self.color)
        self.frame3.pack(pady=5, fill=BOTH, expand=1)
        self.frame3.pack_propagate(0)
        self.hddState = Label(self.frame3, text='Hard Disk', font="Calibri 15 bold", fg='white', bg='red')
        self.hddState.pack(fill=X)
        self.canvas3 = Canvas(self.frame3)
        self.canvas3.pack(fill=X, expand=1)

        self.CPU_line = self.canvas1.create_line(0, -70, 0, 0, fill="red")
        self.mem_line = self.canvas2.create_line(0, -90, 0, 0, fill="blue")
        self.disk_line = self.canvas3.create_line(0, -90, 0, 0, fill="green")

        self.update_plot()

    def getCPUpercent(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > 50:
            winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
        return int(cpu_usage)
    def getMemorypercent(self):
        mem_usage = psutil.virtual_memory().percent
        if mem_usage > 85:
            winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
        return int(mem_usage)
    def getDiskpercent(self):
        disk_usage = psutil.disk_usage('C:\\').percent
        if disk_usage > 85:
            winsound.PlaySound('sound.wav', winsound.SND_FILENAME)
        return int(disk_usage)

    def getMemoryInfo(self):
        mem_info = psutil.virtual_memory()
        return '(Used:'+str(mem_info.used) + ' '+ 'Free:' + str(mem_info.available) + ')'
    def getDiskInfo(self):
        allDisks = ''
        for disk_details in psutil.disk_partitions():
            disk_name = disk_details.mountpoint
            disk_info = psutil.disk_usage(disk_name)
            allDisks += '('+ disk_name + ' '+ 'Used:' + str(disk_info.used) + ' ' + 'Free' + str(disk_info.free)+') '
        return allDisks


    def update_plot(self):
        c = -self.getCPUpercent()
        m = -self.getMemorypercent()
        d = -self.getDiskpercent()

        #print self.canvas1.winfo_height()

        self.add_point(self.CPU_line, c, self.canvas1)
        self.add_point(self.mem_line, m, self.canvas2)
        self.add_point(self.disk_line, d, self.canvas3)

        self.canvas1.xview_moveto(1.0)
        self.canvas2.xview_moveto(1.0)
        self.canvas3.xview_moveto(1.0)

        ram_info = self.getMemoryInfo()
        disk_info = self.getDiskInfo()

        self.cpuState.config(text= 'CPU: ' + str(abs(c))+"%")
        self.memState.config(text= 'Memory: ' + str(abs(m))+"%" + ram_info)
        self.hddState.config(text= 'Hard Disk: ' + str(abs(d))+"%" + disk_info)

        self.after(1, self.update_plot)

    def add_point(self, line, y, canvas):
        coords = canvas.coords(line)
        x = coords[-2] + 1
        coords.append(x)
        coords.append(y)
        coords = coords[-(screenWidth * 2):]  # keep # of points to a manageable size
        canvas.coords(line, *coords)
        canvas.configure(scrollregion=canvas.bbox("all"))


if __name__ == '__main__':
    root = tk.Tk()
    root.state("zoomed")
    root.title('System Monitor')
    o = monitorPage(root, 'white').pack()
    root.geometry('1024x520+70+30')
    root.mainloop()