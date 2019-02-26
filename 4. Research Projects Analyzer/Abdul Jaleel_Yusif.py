from Tkinter import*
import ttk, tkFileDialog,tkMessageBox,re,urllib2,unicodedata,encodings,base64,urllib,os,PIL
from bs4 import BeautifulSoup
from urllib2 import urlopen
from PIL import Image,ImageTk
baseurl = "http://cs.sehir.edu.tr/"
years=["All Years"]
p_investigators=["All Investigators"]
f_institutions=["All Institutions"]
all_data=[]
images_list=[]

class Project_4(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.frame1=Frame(self)
        self.frame1.pack(fill=X)
        self.frame1a=Frame(self.frame1)
        self.frame1a.pack(fill=X)
        self.frame1b=Frame(self.frame1)
        self.frame1b.pack(fill=X, pady=2,padx=5)
        self.frame1c=Frame(self.frame1)
        self.frame1c.pack(fill=X)

        self.frame2=Frame(self)
        self.frame2.pack(fill=X)
        self.frame2a=Frame(self.frame2)
        self.frame2a.pack(side=LEFT,fill=X,pady=10)

        self.frame3=Frame(self)
        self.frame3.pack(fill=X)
        self.frame3a=Frame(self.frame3)
        self.frame3a.pack(side=LEFT,fill=X,padx=10, anchor=N)
        self.frame3b=Frame(self.frame3)
        self.frame3b.pack(side=LEFT,fill=X,padx=30,anchor=N,pady=5)
        self.frame3c=Frame(self.frame3)
        self.frame3c.pack(side=LEFT,fill=X)
        self.frame3d=Frame(self.frame3)
        self.frame3d.pack(side=LEFT,fill=Y)


        self.frame4=Frame(self)
        self.frame4.pack(fill=X)
        self.frame4a=Frame(self.frame4)
        self.frame4a.pack(fill=X,anchor=N)
        self.frame4b=Frame(self.frame4)
        self.frame4b.pack(fill=X,anchor=E)

        self.frame5=Frame(self)
        self.frame5.pack(fill=BOTH,expand=1)
        self.frame5a = Frame(self.frame5)
        self.frame5a.pack(side=LEFT,fill=BOTH, expand=1,anchor=NW,padx=5)
        self.frame5b = Frame(self.frame5)
        self.frame5b.pack(side=LEFT,fill=BOTH, expand=1,anchor=NE)

        self.initUI()



    def initUI(self):
        self.parent.title("SEHIR Research Projects Analyzer")
        self.pack(fill=BOTH, expand = True)

        heading = Label (self.frame1a, text = "SEHIR Research Projects Analyzer - CS Edition", fg = "white", bg = "cyan4",font = ("Georgia",18))
        heading.pack(fill=X)

        label1=Label(self.frame1b,font = ("Georgia",12),text = "Please provide a URL :")
        label1.pack(side=LEFT,fill=X, pady=2,padx=1)
        entryvar= StringVar()
        self.entry1=Entry(self.frame1b, bg= 'white', fg='blue',font = (" ",12),textvariable=entryvar)
        self.entry1.pack(side=LEFT,fill=X,ipady=3,ipadx=220,pady=5,padx=2)
        entryvar.set("http://cs.sehir.edu.tr/en/research/")
        fetch_button = Button(self.frame1b, font = ("",12),text = "Fetch Research Projects", command= self.fetching_data)
        fetch_button.pack(side=LEFT,fill=X,padx=2,pady=2)
        separator1=Label(self.frame1c,text = "."*500)
        separator1.pack(fill=X,anchor=N)

        label2=Label(self.frame2a,font = ("Georgia",12,"bold"),fg='navy',text = "Filter Research Projects By:")
        label2.pack(side=LEFT,fill=X,padx=15,anchor=NW)
        label2a=Label(self.frame2a,font = ("Georgia",12,"bold"),fg='navy',text = "Fetch Research Projects:")
        label2a.pack(side=LEFT,fill=X,padx=145)


        label3=Label(self.frame3a,font = (" ",11,"bold"),fg='green3',text = "Year:")
        label3.pack(pady=3,padx=5,anchor=NW)
        label4=Label(self.frame3a,font = (" ",11,"bold"),fg='green3',text = "Principal Investigator:")
        label4.pack(pady=5,padx=5,anchor=NW)
        label5=Label(self.frame3a,font = (" ",11,"bold"),fg='green3',text = "Funding Institution:")
        label5.pack(pady=3,padx=5,anchor=NW)



        self.c_box1= ttk.Combobox(self.frame3b)
        self.c_box1.pack(fill=X)
        self.c_box2= ttk.Combobox(self.frame3b)
        self.c_box2.pack(fill=X,pady=10)
        self.c_box3= ttk.Combobox(self.frame3b)
        self.c_box3.pack(fill=X)
        display_button = Button(self.frame3b, font = ("",11),text = "Display Project Titles", command = self.DisplayButton)
        display_button.pack(fill=X,pady=5)


        self.listbox1= Listbox(self.frame3c, height=5,width=100)
        self.listbox1.pack(fill=X)
        description_button = Button(self.frame3c, font = ("",11),text = "Show Description", command = self.ShowDescription)
        description_button.pack(pady=5,anchor=W)

        scroll_bar1= ttk.Scrollbar(self.frame3d)
        scroll_bar1.pack(anchor=E,fill=Y,ipady=18)
        scroll_bar1.config(command=self.listbox1.yview)

        separator2 = Label(self.frame4a,text = "."*500)
        separator2.pack(fill=X, anchor=N)

        label6=Label(self.frame4b,font = ("Georgia",12,"bold"),fg='blue4',text = " "*150 + "Project Description:")
        label6.pack(fill=X,padx=50,anchor=E)

        self.text1 = Label(self.frame5a, width=75, bg="white")
        self.text1.pack(side=LEFT,fill=BOTH, expand=1, anchor=W,pady=5,padx=5)
        self.text2= Text(self.frame5b,width=50,height=50,bg= 'white',font=('Helvetica', 10),exportselection=0)
        self.text2.pack(side=LEFT,fill=BOTH,expand=1,pady=5)
        scroll_bar2= ttk.Scrollbar(self.frame5)
        scroll_bar2.pack(side=RIGHT,fill=Y)
        scroll_bar2.config(command=self.text2.yview)

    def fetching_data(self):

        try:
            url = self.entry1.get() #gets the url from entry widget, default is the website for this project
            soup = BeautifulSoup(urllib2.urlopen(url).read(),"html.parser")
            f_data = soup.find_all("li", {"class":"list-group-item"})  #data for all projects
            images = soup.find_all("img")           #images for all projects
            for image in images[1:]:                #slicing out the first image because it does not belong to a project
                img = image.get("src")              #getting image link
                normal_image = str(img)             #converting it to string
                images_list.append(normal_image)
            for data in f_data:
                bucket = []
                for i in range(3,14):               #getting only the relevant data needed because 0,1,2 are not needed,0 and 2 are empty strings
                    print data.contents[0]
                    a = data.contents[i]
                    try:
                        b = a.text.replace("\n","").replace("\r","")
                        c = b.encode('utf-8')
                        if len(c) > 2:
                            bucket.append(c)
                    except:
                        continue
                all_data.append(bucket)
        except ValueError:
            tkMessageBox.showinfo("Error!", "Please make sure you provided a correct URL and also check your connection")
        #adding image links
        for i in range(len(all_data)):
            all_data[i].append(images_list[i])
        # population year combobox
        yillar = []
        for data in all_data:
            date = data[1].split(" ")
            for item in date:
                if "2" in item and item not in yillar:  #extracting only the years
                    yillar.append(item)
        yil= sorted(yillar)
        years.extend(yil)                               #adding list of years to years list defined above
        self.c_box1["values"] = years
        self.c_box1.current(0)                          #sets current year in combobox to "All years"
        # populating Principal investigator combox
        ptors=[]
        for data in all_data:
            investigator = data[3].split("   ")         #getting names of investigators
            for item in investigator:
                item=item.decode("utf-8")               #decoding it since it was encoded initially
                if ":" not in item and item not in ptors and item != "":  #filtering out only name and surname
                    ptors.append(item)
        ptors.sort(key=lambda x: x.split()[1])              #sorting according to surnames
        p_investigators.extend(ptors)
        self.c_box2["values"] = p_investigators
        self.c_box2.current(0)
        # populating funding institution combox
        fi =[]
        for data in all_data:
            f_inst = data[2].split(": ")
            if f_inst[1] not in fi:
                fi.append(f_inst[1])
        f_institutions.extend(sorted(fi))
        self.c_box3["values"] = f_institutions
        self.c_box3.current(0)


    def DisplayButton(self):
        self.listbox1.delete(0,END)    #making sure that listbox is updated each times the button is clicked
        #getting combobox values
        year_val= self.c_box1.get()
        pi_val = self.c_box2.get()
        fi_val = self.c_box3.get()
        def get_title(val,n):         #function for getting titles of projects that match combobox selections
            #val is the value of combobox item (!All) and n is its index the data list
            titles = []
            for data in all_data:
                if val in data[n].decode("utf-8"):
                    titles.append(data[0])
            return titles
        def one_appender(liste):                #function for inserting titles in listbox, when only 1 of the combobox value is not "All"
            for el in liste:
                self.listbox1.insert(END,el)
        def two_appender(list1,list2):          #function for inserting titles in listbox, when two of the combobox values is not "All"
            for title in list1:
                if title in list2:
                    self.listbox1.insert(END,title)
        if year_val == "All Years" and pi_val == "All Investigators" and fi_val == "All Institutions":
            for data in all_data:
                titles = data[0]
                self.listbox1.insert(END,titles)
        elif year_val == "All Years" and pi_val == "All Investigators" and fi_val != "All Institutions":
            titles = get_title(fi_val,2)
            one_appender(titles)
        elif year_val == "All Years" and pi_val != "All Investigators" and fi_val == "All Institutions":
            titles = get_title(pi_val,3)
            one_appender(titles)
        elif year_val != "All Years" and pi_val == "All Investigators" and fi_val == "All Institutions":
            titles = get_title(year_val,1)
            one_appender(titles)
        elif year_val != "All Years" and pi_val != "All Investigators" and fi_val == "All Institutions":
            titles1 = get_title(pi_val,3)
            titles2 = get_title(year_val,1)
            two_appender(titles1,titles2)
        elif year_val != "All Years" and pi_val == "All Investigators" and fi_val != "All Institutions":
            titles1 = get_title(year_val,1)
            titles2 = get_title(fi_val,2)
            two_appender(titles1,titles2)
        elif year_val == "All Years" and pi_val != "All Investigators" and fi_val != "All Institutions":
            titles1 = get_title(pi_val,3)
            titles2 = get_title(fi_val,2)
            two_appender(titles1,titles2)
        else:
            titles1 = get_title(year_val,1)
            titles2 = get_title(fi_val,2)
            titles3 = get_title(pi_val,3)
            for title in titles1:
                if title in titles2 and title in titles3:
                    self.listbox1.insert(END,title)

    def ShowDescription(self):
        try:
            self.text2.delete('1.0',END)     #making sure description refreshes each time button is clicked
            self.text1.destroy()             #refreshing image for each topic selection
            self.text1 = Label(self.frame5a, width=75, bg="white")
            self.text1.pack(side=LEFT,fill=BOTH, expand=1, anchor=W,pady=5,padx=5)
            indx =self.listbox1.curselection()
            selected_title = self.listbox1.get(indx)

            #getting image
            for data in all_data:               #fetching the url for the image of the selected topic
                if selected_title in data[0]:
                    url = baseurl+data[5]
            name = "myimage.png"
            urllib.urlretrieve(url, name)           #getting image from online
            img_org = Image.open(name)
            width_org, height_org = img_org.size
            # resizing image
            factor = 0.80
            width = int(width_org * factor)
            height = int(height_org * factor)
            img_anti = img_org.resize((width, height), Image.ANTIALIAS)
            name, ext = os.path.splitext(name)
            new_name = "%s%s%s" % (name, "1", ext)
            img_anti.save(new_name)
            photo = ImageTk.PhotoImage(img_anti)
            pic_label = Label(self.text1,image=photo)
            pic_label.image = photo                     #keeping a reference
            pic_label.pack(fill=BOTH, expand=1)

            #writing description
            for data in all_data:
                if selected_title in data[0]:
                    description = data[4]
                    self.text2.insert(END,description)
        except TclError:
            tkMessageBox.showinfo("Error!", "Please select a project title")




def main():
    root = Tk()
    root.geometry("1200x600+50+20")
    app = Project_4(root)
    root.mainloop()
main()