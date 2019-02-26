from Tkinter import*
from PIL import Image, ImageTk
from tkColorChooser import askcolor
import ttk, tkFileDialog,tkMessageBox,random

class Project_7(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.frame1=Frame(self)
        self.frame1.pack(fill=X)
        self.frame2=Frame(self)
        self.frame2.pack(anchor = CENTER)
        self.frame3 = Frame(self)
        self.frame3.pack(fill = Y)
        self.initUI()

    def initUI(self):
        self.parent.title("My Paint")
        self.pack(fill=BOTH, expand = True)
        #labels for fill color and border color
        self.fcolor = "green"
        self.bcolor = "red"

        heading = Label (self.frame1, text = "My Paint", fg = "white", bg = "blue4",font = ("Georgia",18))
        heading.pack(fill=X)

        self.photo1 = ImageTk.PhotoImage(Image.open("assets/rectangle.png"))
        self.rectangle = Label(self.frame2,image=self.photo1, relief = RAISED, width = 25, height = 25)
        self.rectangle.image = self.photo1  #keeping reference
        self.rectangle.pack(side = LEFT)
        self.rectangle.bind("<Button-1>",self.Rectangle)

        self.photo2 = ImageTk.PhotoImage(Image.open("assets/oval.png"))
        self.oval = Label(self.frame2, image = self.photo2, relief = RAISED, width = 25, height = 25)
        self.oval.image = self.photo2       #keeping reference
        self.oval.pack(side = LEFT)
        self.oval.bind("<Button-1>",self.Oval)

        self.photo3 = ImageTk.PhotoImage(Image.open("assets/line.png"))
        self.line = Label(self.frame2, image = self.photo3, relief = RAISED, width = 25, height = 25)
        self.line.image = self.photo3       #keeping reference
        self.line.pack(side = LEFT)
        self.line.bind("<Button-1>",self.Line)

        self.photo4 = ImageTk.PhotoImage(Image.open("assets/drag.png"))
        self.drag = Label(self.frame2, image = self.photo4, relief = RAISED, width = 25, height = 25)
        self.drag.image = self.photo4       #keeping reference
        self.drag.pack(side = LEFT)
        self.drag.bind("<Button-1>",self.Drag)

        self.photo5 = ImageTk.PhotoImage(Image.open("assets/eraser.png"))
        self.eraser = Label(self.frame2, image = self.photo5, relief = RAISED, width = 25, height = 25)
        self.eraser.image = self.photo5     #keeping reference
        self.eraser.pack(side = LEFT)
        self.eraser.bind("<Button-1>",self.Eraser)

        fillcolor = Label(self.frame2, text = "Fill Color:",font = ("",10))
        fillcolor.pack(side = LEFT)
        self.fc = Label(self.frame2, bg = self.fcolor, width = 3)
        self.fc.pack(side = LEFT)
        self.fc.bind("<Button-1>",self.fColor)

        bordercolor = Label(self.frame2, text = "Border Color:",font = ("",10))
        bordercolor.pack(side = LEFT)
        self.bc = Label(self.frame2, bg = self.bcolor, width = 3)
        self.bc.pack(side = LEFT)
        self.bc.bind("<Button-1>",self.bColor)

        label6 = Label(self.frame2, text = "Weight:",font = ("",10))
        label6.pack(side = LEFT)
        var = StringVar()
        var.set("4")            #default value
        self.weight = Spinbox(self.frame2, from_= 1, to=100, width = 2, textvariable = var)
        self.weight.pack(side = LEFT)
        #Button for bonus part
        beautify = ttk.Button(self.frame2, text="Beautify Layout", command = self.beautify_layout)
        beautify.pack(side = LEFT, padx=10)

        self.canvas = Canvas(self.frame3, bg = "white", height = 800, width = 950)
        self.canvas.pack(fill = Y)
        self.Rectangle(1)       #to initialize rectangle tool when the program is opened for the first time

    def fColor(self,event):
        color = askcolor()
        if None not in color:                   #preventing color from changing (to white) when no color is chosen
            self.fc.config(bg = color[1])       #changing label color for fill color
            self.fcolor = color[1]              #changing fill color for tools

    def bColor(self,event):
        color = askcolor()
        if None not in color:                   #preventing color from changing (to black) when no color is chosen
            self.bc.config(bg = color[1])       #changing label color for border color
            self.bcolor = color[1]              #changing border color for tools

    def Rectangle(self,event):              #Rectangle tool and its events
        self.clicked(self.rectangle)
        self.dragging = False
        self.canvas.bind('<ButtonPress-1>', self.create_rectangle)
        self.canvas.bind('<B1-Motion>', self.canvasDrag)
        self.canvas.bind('<ButtonRelease-1>', self.canvasDrop)
        self.drawing = False

    def Oval(self,event):                   #oval tool and its events
        self.clicked(self.oval)
        self.dragging = False
        self.canvas.bind('<ButtonPress-1>', self.create_oval)
        self.canvas.bind('<B1-Motion>', self.canvasDrag)
        self.canvas.bind('<ButtonRelease-1>', self.canvasDrop)
        self.drawing = False

    def Line(self,event):                   #line tool and its events
        self.clicked(self.line)
        self.dragging = False
        self.canvas.bind('<ButtonPress-1>', self.create_line)
        self.canvas.bind('<B1-Motion>', self.canvasDrag)
        self.canvas.bind('<ButtonRelease-1>', self.canvasDrop)
        self.drawing = False

    def Drag(self,event):                   #drag tool
        self.clicked(self.drag)
        self.dragging = True
        self.canvas.bind('<ButtonPress-1>', self.itemSelect)
        self.canvas.bind('<B1-Motion>', self.itemDrag)
        self.canvas.bind('<ButtonRelease-1>', self.itemDrop)

    def Eraser(self,event):                 #eraser tool
        self.clicked(self.eraser)
        self.drawing = False
        self.canvas.bind('<Button-1>', self.remove_obj)

    def clicked(self,icon):                 #changing relief of tool buttons when clicked
        liste = [self.rectangle, self.oval, self.line, self.drag, self.eraser]
        icon.config(relief = FLAT)
        if icon != self.drag and icon != self.eraser:
            self.canvas.config(cursor = "tcross")       #changing cursor for rectangle, oval and line tool
        elif icon == self.eraser:
            self.canvas.config(cursor = "X_cursor")     #changing cursor for eraser
        else:
            self.canvas.config(cursor = "hand2")        #changing cursor for drag tool
        for i in liste:
            if i != icon:
             i.config(relief = RAISED)

    #Event for the Drag tool
    def itemSelect(self, event):
        #Selecting item for dragging
        self.dragging = True
        self.dragx, self.dragy = event.x, event.y
        self.dragitem = self.canvas.find_closest(event.x, event.y)

    def itemDrag(self, event):
        #Moving item using the pixel coordinates in the event object.
        if not self.dragging:
            return
        dx = event.x - self.dragx
        dy = event.y - self.dragy
        self.canvas.move(self.dragitem, dx, dy)
        self.dragx, self.dragy = event.x, event.y

    def itemDrop(self, event):
        #Droping item
        if not self.dragging:
            return
        self.dragging = False

    def create_rectangle(self, event):      #drawing rectangle
        if self.dragging:
            return
        self.drawing = True
        self.startx, self.starty = event.x, event.y
        item = self.canvas.create_rectangle(self.startx, self.starty, event.x, event.y, outline=self.bcolor,
                                            fill=self.fcolor, width=self.weight.get())

        self.shape = item

    def create_oval(self, event):           #drawing oval
        if self.dragging:
            return
        self.drawing = True
        self.startx, self.starty = event.x, event.y
        item = self.canvas.create_oval(self.startx, self.starty, event.x, event.y, outline=self.bcolor,
                                       fill=self.fcolor, width=self.weight.get())

        self.shape = item

    def create_line(self, event):           #line tool
        if self.dragging:
            return
        self.drawing = True
        self.startx, self.starty = event.x, event.y
        item = self.canvas.create_line(self.startx, self.starty, event.x, event.y, fill=self.fcolor, width=self.weight.get())

        self.shape = item

    def canvasDrag(self, event):            #event for mouse motion when drawing
        if self.drawing:
            item = self.canvas.find_closest(event.x, event.y)
            self.canvas.coords(self.shape, self.startx, self.starty, event.x, event.y)

    def canvasDrop(self, event):            #event for dropping object on canvas after drawing
        if self.drawing:
            self.drawing = False

    def remove_obj(self,event):             #event for eraser tool
        for i in self.canvas.find_closest(event.x,event.y):
            self.canvas.delete(i)

    def beautify_layout(self):              #Bonus button
        all = self.canvas.find_all()
        d = []
        for i in all:
            coords = self.canvas.coords(i)
            newcoords = self.hillclimb(coords)
            self.canvas.coords(i,newcoords[0],newcoords[1],newcoords[2],newcoords[3])


    def hillclimb(self,domain):
        # Create a random solution
        sol = [random.randint(min(domain), max(domain))
               for i in range(4)]

        # Main loop
        for x in range(1000):
            # Create list of neighboring solutions
            neighbors = []
            for j in range(len(domain)):
                # One away in each direction
                if sol[j] > domain[j]:
                    neighbors.append(sol[0:j] + [sol[j] - 1] + sol[j + 1:])
                if sol[j] < domain[j]:
                    neighbors.append(sol[0:j] + [sol[j] + 1] + sol[j + 1:])

        return neighbors[-1]

def main():
    root = Tk()
    root.geometry("1000x600+120+20")
    app = Project_7(root)
    root.mainloop()
main()