from Tkinter import*
import ttk, tkFileDialog,tkMessageBox,anydbm,xlrd,pickle

semesters_tuple = ('Semester 1', 'Semester 2', 'Semester 3', 'Semester 4', 'Semester 5', 'Semester 6', 'Semester 7', 'Semester 8')

class Project_1(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.parent.title("Curriculum Viewer v1.0")
        self.initUI()
        self.combo_box()

    def initUI(self):
        self.grid()
        heading = Label (self, text = "Curriculum Viewer v1.0", fg = "white", bg = "green", width=35, height = 2,font = ("",25))
        heading.grid(row = 0,column=0, columnspan=2, sticky = EW)
        label1 = Label (self, text = "Please select curriculum excel file:")
        label1.grid(row = 1,column= 0, sticky= E, padx = 3, pady = 2)
        browse = Button(self,text = "Browse",command = self.browse)
        browse.grid(row=1,column=1, sticky = W, padx = 3, pady = 2)
        label2 = Label (self, text = "Please select semester that you want to print:")
        label2.grid(row=2,column=0, sticky = E, padx = 3, pady = 2)
        display = Button(self,text = "Display",command = self.display, width = 10)
        display.grid(row=4,column=1, sticky = W, padx = 3, pady = 2)

        self.file_opt = options = {}    # source ---> http://tkinter.unpythonic.net/wiki/tkFileDialog
        options['filetypes'] = [('Excel Files',('.xlsx','.xls'))]
        options['initialdir'] = 'C:\\'
        options['title'] = 'Choose your excel file'

        self.frame2 = Frame()
        self.frame2.grid(row=11,column=0, sticky = W+E+N+S,columnspan=2)

    def combo_box(self):   # source ---> http://stackoverflow.com/questions/17757451/simple-ttk-combobox-demo
        self.combo_box_val = StringVar()
        self.mybox = ttk.Combobox(self, textvariable= self.combo_box_val)
        self.mybox['values'] = semesters_tuple
        self.mybox.current(0)
        self.mybox.bind("<<ComboboxSelected>>",self.selectedcombo)
        self.mybox.grid(row=2,column=1, sticky = W, padx = 3, pady = 2)

    def selectedcombo(self,event):

        return self.mybox.get()


    def browse(self):
        try:
            self.excel_file = tkFileDialog.askopenfilename(**self.file_opt)   # source ---> http://tkinter.unpythonic.net/wiki/tkFileDialog
            workbook = xlrd.open_workbook(filename=self.excel_file)
            sheet = workbook.sheet_by_index(0)
        except IOError:   #error handler for cases when user directly clicks on display without choosing a file
            return

        def get_values(x,y,col):   #function for getting values from excel file
            kod=[]
            title=[]
            cred=[]
            sem_vals=[kod,title,cred]
            for i in range(3):
                for r in range(x,y):
                    if i==0:
                        self.element = sheet.cell_value(r,col)
                        kod.append(self.element)
                    elif i==1:
                        self.element = sheet.cell_value(r,col+1)
                        title.append(self.element)
                    else:
                        self.element = sheet.cell_value(r,col+5)
                        cred.append(self.element)
            return sem_vals

        sem_1 = get_values(6,13,0)
        sem_2 = get_values(6,15,8)
        sem_3 = get_values(18,24,0)
        sem_4 = get_values(18,26,8)
        sem_5 = get_values(29,35,0)
        sem_6 = get_values(29,37,8)
        sem_7 = get_values(41,46,0)
        sem_8 = get_values(41,46,8)

        sem_list=[sem_1,sem_2,sem_3,sem_4,sem_5,sem_6,sem_7,sem_8]

        sem_dict={}
        for i in range(len(semesters_tuple)):
            sem_dict[semesters_tuple[i]]= sem_list[i]

        db = anydbm.open('curriculum.db', 'n')
        pickled1 = pickle.dumps(sem_dict)
        db["dictionary"] = pickled1
        db.close()

    def display(self):
        try:
            self.frame2.destroy()
            selected_semester = self.selectedcombo(event=0) # To know which item was selected in combobox
            db = anydbm.open("curriculum.db", 'r')
            for key in db:
                loaded = pickle.loads(db[key])
            self.frame2 = Frame()
            self.frame2.grid(row=11,column = 0,sticky = W+E+N+S,columnspan=2)

            for k in loaded:
                if k == selected_semester:
                    for i in range (3):
                        semLoaded1= loaded[k][i]
                        count = 5
                        if i == 0:
                            coursecode = Label(self.frame2, text="Course Code",font = ("",13))
                            coursecode.grid(row=2,column=0, rowspan=3,padx=5,sticky=W)
                            for item in semLoaded1:
                                if item != '':
                                    Label(self.frame2, text=item,fg="red").grid(row=count,column= 0,sticky=W)
                                    count +=1
                        elif i == 1:
                            coursetitle = Label(self.frame2, text="Course Title",font = ("",13))
                            coursetitle.grid(row=2,column=i, rowspan=3,padx=35)
                            for item in semLoaded1:
                                if "=" not in item:
                                    Label(self.frame2, text=item,fg="red").grid(row=count,column= i,rowspan=1, sticky=W)
                                    count +=1
                        elif i == 2:
                            coursecode = Label(self.frame2, text="Credit",font = ("",13))
                            coursecode.grid(row=2,column=i, rowspan=3,padx=35)
                            for item in semLoaded1:
                                if item <5 and item !="" :
                                    Label(self.frame2, text=item,fg="red").grid(row=count,column= i)
                                    count +=1
                                else:
                                    if count == 12:
                                        count -=1
                                    Label(self.frame2, text="").grid(row=count,column= i)
            db.close()
        except :
            tkMessageBox.showinfo("Error!", "A curriculum file should be selected first by clicking on the Browse button.") #Error handler

def main():
    root = Tk()
    root.geometry("630x400+200+200")
    app = Project_1(root)
    root.mainloop()
main()