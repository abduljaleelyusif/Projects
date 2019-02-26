from Tkinter import*
from clusters import*
import ttk, tkFileDialog,tkMessageBox,re

class Project_3(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.frame1=Frame(self)
        self.frame1.pack(fill=X)
        self.frame2=Frame(self)
        self.frame2.pack(fill=X)
        self.frame3=Frame(self)
        self.frame3.pack(fill=X)
        self.frame4=Frame(self,bd=2, relief=SOLID)
        self.frame4.pack(fill=BOTH, expand = 1,padx= 50,pady=30)
        self.frame4a=Frame(self.frame4)
        self.frame4a.pack(fill=X)
        self.frame4b=Frame(self.frame4)
        self.frame4b.pack(fill=BOTH,expand=1)
        self.frame5=Frame(self.frame4a)
        self.frame5.pack(fill=X)
        self.frame5a=Frame(self.frame5)
        self.frame5a.pack(fill=X,side=LEFT,padx=30)
        self.frame5b=Frame(self.frame5)
        self.frame5b.pack(fill=X,side=LEFT)
        self.frame5c=Frame(self.frame5)
        self.frame5c.pack(fill=X,side=LEFT,padx=70)
        self.frame6=Frame(self.frame4a)
        self.frame6.pack(fill=X,padx=150,pady=5)
        self.initUI()
        self.MyCanvas()



    def initUI(self):
        self.parent.title("Course Analyzer - Sehir Limited Edition")
        self.pack(fill=BOTH, expand = True)

        heading = Label (self.frame1, text = "COURSE ANALYSER - SEHIR LIMITED EDITION", fg = "white", bg = "cyan3",font = ("",18))
        heading.pack(fill=X)

        label1 = Label (self.frame2, font = ("",12),text = "Upload a file that contains course discription:")
        label1.pack(side=LEFT, padx = 100,pady=10)
        browse = Button(self.frame2, font = ("",12),text = "Browse",command=self.browse)
        browse.pack(side=LEFT,pady=10)

        label2 = Label (self.frame3, font = ("",12),text = "Selected file:")
        label2.pack(side=LEFT, padx = 100)
        self.label3 = Label(self.frame3, relief = "solid")
        self.label3.pack(side=LEFT,ipadx=50)

        label4 = Label(self.frame5a, font = ("",10),text = 'Similarity Measure:')
        label4.pack(side=LEFT,padx=50,pady=10)

        self.measure_var = IntVar()
        rb1= Radiobutton(self.frame5b, text="Pearson", variable = self.measure_var, value=1)
        rb1.pack(pady=15,anchor=W)
        rb2= Radiobutton(self.frame5b, text="Tanimoto", variable = self.measure_var,value=2)
        rb2.pack(pady=5)

        label4 = Label(self.frame5c, font = ("",10),text = 'Select Course Codes:')
        label4.pack(side=LEFT,padx=5,pady=10)
        self.list_box= Listbox(self.frame5c, height=5, selectmode=MULTIPLE)
        self.list_box.pack(side=LEFT,pady=15)
        scroll_bar=Scrollbar(self.frame5c)
        scroll_bar.pack(side=LEFT,pady=15,ipady=16)
        scroll_bar.config(command=self.list_box.yview)

        button1 = Button(self.frame6, text ='Draw Hierarchical Cluster Diagram',command = self.draw_hcd)
        button1.pack(side=LEFT,padx=5)
        button2 = Button(self.frame6, text ='Print Hierarchical Cluster as Text',comman= self.print_hct)
        button2.pack(side=LEFT,padx=5)
        button3 = Button(self.frame6, text ='Show Data Matrix',command=self.show_datamatrix)
        button3.pack(side=LEFT,padx=5)

        self.file_opt = options = {}                        # source ---> http://tkinter.unpythonic.net/wiki/tkFileDialog
        options['filetypes'] = [('Text Files','.txt')]
        options['initialdir'] = 'C:\\'
        options['title'] = 'Please choose your file'
        self.wordcount = {}
    def browse(self):
        try:
            self.courses=[]
            self.filename = tkFileDialog.askopenfilename(**self.file_opt)   # source ---> http://tkinter.unpythonic.net/wiki/tkFileDialog
            self.label3.config(text=self.filename)                          #dynamically displays the path for the selected file
            openedfile = open(self.filename,'r')
            for line in openedfile:
                extracted = re.findall(r'\w+\s\d{3}\D?',line)    #filtering out course codes from text file
                if len(extracted)==1 and extracted[0] not in self.courses and extracted[0] != 'PHYS 203 ' and extracted[0] != 'MATH 201 ':   #this is to make sure that a course does not appear more than one time in the list
                    #also MATH 201 and PHYS 203 seem to be a typo in the given file, so they were excluded from the dictionary
                    self.courses.append(extracted[0])
            codes=[]
            for course in self.courses:
                course_code= course.split(" ")        #splitting the alpha part of the course codes
                if course_code[0] not in codes:
                    codes.append(course_code[0])
            self.list_box.delete(0,END)               #this is to make sure that when a file is opened and another is opened again, the listbox displays the related courses
            for item in sorted(codes):
                self.list_box.insert(END,item)        #populating the listbox with the course codes
            openedfile.close()
        except IOError:   #error handler for cases when user clicks on browse but does not choose a file
            pass
    #draw_hcd(),print_hct() and show_datamatrix() methods contain error handlers in cases where the user clicks on their button without selecting a course from the listbox
    def draw_hcd(self):
        try:
            self.gatheringData()
            self.frame.destroy()
            self.MyCanvas(self.width,self.height)
            rname,colname,vectors=readfile('Data Matrix.txt')
            siralama=hcluster(vectors,self.sim_measure)
            self.create_dendrogram(siralama,rname)
        except:
            tkMessageBox.showinfo("Error!", "Please make sure you have selected a file and chosen some courses")

    def print_hct(self):
        try:
            self.gatheringData()
            self.frame.destroy()
            self.MyCanvas(25,self.height+550)
            rname,colname,vectors=readfile('Data Matrix.txt')
            siralama=hcluster(vectors,self.sim_measure)
            new_clust = clust2str(siralama,rname,)
            self.my_canvas.create_text(0,0,text = new_clust,anchor='nw')
        except:
            tkMessageBox.showinfo("Error!", "Please make sure you have selected a file and chosen some courses")

    def show_datamatrix(self):
        try:
            self.gatheringData()
            self.frame.destroy()
            self.MyCanvas(self.width,self.height)
            list_of_lines = []
            y=1
            dMatrix = open('Data Matrix.txt','r')
            for lines in dMatrix:
                line = lines.strip()
                list_of_lines.append(line)
            self.my_canvas.create_text(1,y,text = list_of_lines[0],anchor='nw') #first print column names on the canvas
            for line in sorted(list_of_lines[1:]):
                y+=20
                self.my_canvas.create_text(1,y,text = line,anchor='nw')         #then print courses and their vectors after sorting them
            dMatrix.close()
        except:
            tkMessageBox.showinfo("Error!", "Please make sure you have selected a file and chosen some courses")

    def gatheringData(self):
        a,b,c = readfile(self.filename)    #this returns a list of course names and their descriptions as value of variable a
        about_course = []
        for i in range(0,len(a)-1,2):      #extracting course descriptions
            about_course.append(a[i])
        about_course.append(a[len(a)-1])
        h=0
        for course in about_course:                     #matching each course to their description in a dictionary
            self.wordcount[self.courses[h]]= course
            h +=1
        #Comfirming similarity measure selected (default is pearson)
        if self.measure_var.get()==2:
            self.sim_measure = tanimoto
        else:
            self.sim_measure = pearson
        selecteditems =self.list_box.curselection()     #list of selected course codes in listbox
        selectedlist=[]
        selected_course={}                              #another cictionary only for the selected courses and their descriptions
        for i in selecteditems:
            a = self.list_box.get(i)
            selectedlist.append(a)
        for item in selectedlist:
            for key in self.wordcount:                  #matching and extracing all courses with the selected codes
                e = key.split(' ')
                if item == e[0]:
                    selected_course[key]= self.wordcount[key]
        create_matrix(selected_course,'Data Matrix.txt')  #this creates a matrix of the selected courses to be analyzed
        list_of_lines = []
        dMatrix = open('Data Matrix.txt','r')
        for lines in dMatrix:
            line = lines.strip()
            list_of_lines.append(line)

        dMatrix.close()
        defWidth = list_of_lines[1].split("\t")
        n = sum(len(s) for s in defWidth)
        self.height = len(list_of_lines)*21            #setting the dimension for the height of the canvas according the number of items to be displayed
        self.width = (len(defWidth)*4*13)+ n*14        #setting the dimension for the width according to the number of items used as column names

    def MyCanvas(self,w=2500,h=1000):
        self.frame=Frame(self.frame4b,width=w,height=h)
        self.frame.pack(fill=BOTH,expand=1)
        self.my_canvas=Canvas(self.frame,bg='white',width=w,height=w,scrollregion=(0,0,w,h))
        h_bar=Scrollbar(self.frame,orient=HORIZONTAL)
        h_bar.pack(side=BOTTOM,fill=X)
        h_bar.config(command=self.my_canvas.xview)
        v_bar=Scrollbar(self.frame,orient=VERTICAL)
        v_bar.pack(side=RIGHT,fill=Y)
        v_bar.config(command=self.my_canvas.yview)
        self.my_canvas.config(width=w,height=h)
        self.my_canvas.config(xscrollcommand=h_bar.set, yscrollcommand=v_bar.set)
        self.my_canvas.pack(side=LEFT,expand=True,fill=BOTH)

    def create_dendrogram(self,clust, labels):     # source: clusters.py (modified to draw dendrogram on the canvas)
        h = self.height
        w = self.width/4
        depth = getdepth(clust)
        # width is fixed, so scale distances accordingly
        scaling = float(w - 150) / depth
        self.my_canvas.create_line(0, h / 2, 10, h / 2)
        # Draw the first node
        self.create_node(clust, 10, (h / 2), scaling, labels)

    def create_node(self,clust, x, y, scaling, labels):    # source: clusters.py
        if clust.id < 0:
            h1 = getheight(clust.left) * 20
            h2 = getheight(clust.right) * 20
            top = y - (h1 + h2) / 2
            bottom = y + (h1 + h2) / 2
            # Line length
            ll = clust.distance * scaling
            # Vertical line from this cluster to children
            self.my_canvas.create_line((x, top + h1 / 2, x, bottom - h2 / 2))
            # Horizontal line to left item
            self.my_canvas.create_line((x, top + h1 / 2, x + ll, top + h1 / 2))
            # Horizontal line to right item
            self.my_canvas.create_line((x, bottom - h2 / 2, x + ll, bottom - h2 / 2))
            # Call the function to draw the left and right nodes
            self.create_node(clust.left, x + ll, top + h1 / 2, scaling, labels)
            self.create_node(clust.right, x + ll, bottom - h2 / 2, scaling, labels)
        else:
            # If this is an endpoint, draw the item label
            self.my_canvas.create_text(x + 5, y - 7, text=labels[clust.id])

def main():
    root = Tk()
    root.geometry("1020x600+150+20")
    app = Project_3(root)
    root.mainloop()
main()