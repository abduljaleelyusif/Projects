from Tkinter import*
from recommendations import *
import ttk, tkFileDialog,tkMessageBox,anydbm,xlrd,pickle, unicodedata

workbook = xlrd.open_workbook(filename="Menu.xlsx")
sheet = workbook.sheet_by_index(0)
food_list = []
price_list = []
for i in range(68):
    if i == 0:
        continue
    el = sheet.cell(i,0).value.encode('utf-8')
    el1 = sheet.cell_value(i,1)
    food_list.append(el)
    price_list.append(el1)
all_users_dict = {} #dictionary containing user's data only
users_dict = {}  #dictionary containing data for user and all other users


class Project_2(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.initUI()
        self.combo_box()

    def initUI(self):
        self.parent.title("Enter the Recommender")
        self.grid(sticky=N+S+E+W)
        self.columnconfigure(0,weight=1)
        self.frame1 = Frame(self)
        self.frame1.grid(row=1,column=0,columnspan=2,sticky=E+W)
        self.frame2 = Frame(self)
        self.frame2.grid(row=2,column=0,columnspan=2,sticky=E+W)
        self.frame2a = Frame(self)
        self.frame2a.grid(row=3,column=0,columnspan=2,sticky=E+W)
        self.frame3 = Frame(self)
        self.frame3.grid(row=4,column=0,columnspan=2,sticky=E+W)
        self.frame4 = Frame(self)
        self.frame4.grid(row=5,column=0,columnspan=2,sticky=E+W)
        heading = Label (self.frame1, text = "Cafe Crown Recommendation Engine - SEHIR Special Edition", fg = "white" ,bg = "orange1",font = ("",24))
        heading.grid(row = 0,column=0, sticky = EW)
        label1 = Label (self.frame1, text = "Welcome!",font = ("Georgia",16))
        label1.grid(row = 1,column=0)
        label2 = Label (self.frame1, text = "Please rate entries that you have had at CC, and we will recommend you what you may like to have",font = ("Georgia",16))
        label2.grid(row = 2,column=0)
        label3 = Label (self.frame1, text = "````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````",font = ("",10))
        label3.grid(row = 3,column=0)



        label4 = Label (self.frame2, text = "Choose a meal:",font = ("",14),fg= "red")
        label4.grid(row = 0,column=0, sticky = W,padx=20)
        label4 = Label (self.frame2, text = "Enter your rating:",font = ("",14),fg= "red")
        label4.grid(row = 0,column=1,padx=50)
        self.rating = Scale(self.frame2, from_=1, to=10, orient = HORIZONTAL)
        self.rating.grid(row=1,column=1,padx=50)
        add_b = Button(self.frame2, text = "Add", fg = "blue4",font = ("Georgia",10), command = self.add_button)
        add_b.grid(row= 1, column=2, ipadx=20, padx=25)
        scrollb1 = Scrollbar(self.frame2)
        scrollb1.grid(row=1,column=5,ipady=25,sticky=E)
        self.listbox1 = Listbox(self.frame2, height = 6, width=6)
        self.listbox1.grid(row=1, column = 3,columnspan = 2, ipadx= 100,sticky = N)
        self.listbox1.config(yscrollcommand = scrollb1.set) #Binds the scrollbar to the listbox
        scrollb1.config(command=self.listbox1.yview) # Allows scrolling in the vertical direction

        remove_b = Button(self.frame2, text = "Remove \nSelected", fg = "red2",font = ("Georgia",10),command= self.remove_button)
        remove_b.grid(row=1, column=6, padx=10,pady=10,ipady = 5,ipadx=5, sticky =W)

        label5 = Label (self.frame2a, text = "```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````",font = ("",10))
        label5.grid(row = 2, columnspan = 5)
        label6 = Label (self.frame2a, text = "Get Recommendations",font = ("Georgia",16))
        label6.grid(row = 3, column=2)
        label7 = Label (self.frame2a, text = "```````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````",font = ("",10))
        label7.grid(row = 4, columnspan = 5)



        label8 = Label (self.frame3, text = "Settings:",fg = "red",font = ("Georgia",14))
        label8.grid(row = 0,column=0, sticky = W, padx=20)
        label9 = Label (self.frame3, text = "Number of recommendations:",fg = "green4",font = (" ",11))
        label9.grid(row = 1,column=0, sticky = W,padx=20)
        self.entry = Entry(self.frame3, width = 2)
        self.entry.grid(row = 1, column=0,sticky = E, padx=20)
        label10 = Label (self.frame3, text = "Choose recommendation method:",fg = "green4",font = (" ",11))
        label10.grid(row = 1,column=1, sticky = W,padx=20)
        self.v1 = IntVar()
        rb1 = Radiobutton(self.frame3, text = "User-Based",variable = self.v1,font = ("Georgia",10), value = 1)
        rb1.grid(row=2,column=1, sticky = W,padx=20)
        rb2 = Radiobutton(self.frame3, text = "Item-Based",variable = self.v1,font = ("Georgia",10),value =2)
        rb2.grid(row=3,column=1, sticky = W,padx=20)
        label10 = Label (self.frame3, text = "Choose Similarity Metric:",fg = "green4",font = (" ",11))
        label10.grid(row = 1,column=2, sticky = W,padx=20)
        self.v2= IntVar()
        rb3 = Radiobutton(self.frame3, text = "Euclidean Score",variable = self.v2,font = ("Georgia",10), value = 1)
        rb3.grid(row=2,column=2, sticky = W,padx=20)
        rb4 = Radiobutton(self.frame3, text = "Pearson Score",variable = self.v2,font = ("Georgia",10),value =2)
        rb4.grid(row=3,column=2, sticky = W,padx=20)
        rb5 = Radiobutton(self.frame3, text = "Jaccard Score",variable = self.v2,font = ("Georgia",10),value =3)
        rb5.grid(row=4,column=2, sticky = W,padx=20)
        rec_button = Button(self.frame3, text = "Get Recommendation", fg = "blue1",font = ("Georgia",10), command = self.getRecommendation)
        rec_button.grid(row= 3, column=3, ipadx=15)
        label11 = Label (self.frame3, text = "`````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````````",font = ("",10))
        label11.grid(row = 5,column=0, columnspan = 5)

        #Getting the names of foodstuffs and their prices from excel file
        workbook = xlrd.open_workbook(filename="Menu.xlsx")
        sheet = workbook.sheet_by_index(0)
        food_list = []
        for i in range(68):
            if i == 0:
                continue
            el = sheet.cell(i,0)  #value.encode('utf-8')
            food_list.append(el)

    def combo_box(self):   # source ---> http://stackoverflow.com/questions/17757451/simple-ttk-combobox-demo
        self.combo_box_val = StringVar()
        self.mybox = ttk.Combobox(self.frame2, textvariable= self.combo_box_val)
        self.mybox['values'] = food_list
        self.mybox.current(0)                                             #display an item from the list
        self.mybox.grid(row=1,column=0, sticky = W, padx = 20,ipadx=20)

    def add_button(self): #Adding item and its corresponding rating to listbox1
        fooditem = self.mybox.get()
        ratingpoint = self.rating.get()
        try:                                        #since some of the fooditems do not contain special characters they are treated as normal strings and not unicode
            normalizedfood = unicodedata.normalize("NFKD",fooditem)
            users_dict[normalizedfood] = ratingpoint
        except TypeError:                           #this raises string errors
            users_dict[fooditem] = ratingpoint

        val = "%s ---> %d" %(fooditem,ratingpoint)
        self.listbox1.insert(END,val)
    def remove_button(self):
        deletedItem = self.listbox1.get(ACTIVE).split(' ---> ')
        d_item = deletedItem[0]
        try:
            d= unicodedata.normalize("NFKD",d_item)
            users_dict.pop(d)
        except TypeError:
            users_dict.pop(d_item)

        self.listbox1.delete(ACTIVE)
    def getRecommendation(self):
        try:
            if len(users_dict)!=0:
                try:
                    db0 = anydbm.open("ownratings.db", "w")       #a database containing a dictionary of user, which also contains dictionary of items and their ratings, updated whenever user makes changes
                    for key,vals in db0.items():
                        pickleload = pickle.loads(vals)
                        for food,rate in users_dict.items():
                            pickleload[food] = pickleload.get(food,rate)
                        repickled = pickle.dumps(pickleload)
                        db0[key] = repickled
                    db0.close()
                except:                                           #exception handler for first time usage
                    db = anydbm.open("ownratings.db", "c")
                    pickled = pickle.dumps(users_dict)
                    db["user"] = pickled
            elif len(users_dict) ==0:
                self.oldratings()
            #using these loops below, users_dict will be populated with data for the user, and other users
            db=anydbm.open("ownratings.db","r")
            for a,d in db.items():
                d = pickle.loads(d)
                for a1,d1 in d.items():
                    all_users_dict.setdefault(a,{})
                    try:
                        na1 = unicodedata.normalize("NFKD",a1)
                        all_users_dict[a][na1] = float(d1)
                    except TypeError:
                        all_users_dict[a][a1] = float(d1)
            db.close()
            db1 = anydbm.open("cc_ratings.db", "r")
            for k,v in db1.items():
                v = pickle.loads(v)
                for k1,val1 in v.items():
                    all_users_dict.setdefault(k,{})
                    try:                                                #normalizing food items in this db, skipping str types to make comparison possible
                        nk1 = unicodedata.normalize('NFKD',k1)
                        all_users_dict[k][nk1]= float(val1)
                    except TypeError:
                        all_users_dict[k][k1]= float(val1)
            db1.close()

            self.check_settings()

        except ValueError:                    #(default settings)error handler when user does not choose any settings. ValEr for entry and UnboundER for algorithms
             tkMessageBox.showinfo("Error!", "Please choose your settings")
    def check_settings(self):
        self.frame4.destroy()
        entryno = int(self.entry.get())          # to know the number of recommendations to display
        similarity = self.v2.get()               #similarity function to be used
        if self.v1.get() ==1:                   # to display either user based results as well as recommendations
            self.frame4 = Frame(self)
            self.frame4.grid(row=5)
            label12 = Label (self.frame4, text = "Result Box (Recommendations):",fg = "yellow",bg = "black",font = (" ",11))
            label12.grid(row = 0,column=0, sticky = W,padx=15,pady=5,columnspan=2)
            scrollb2 = Scrollbar(self.frame4)
            scrollb2.grid(row=1,column=1,ipady=25,sticky = E)
            self.listbox2 = Listbox(self.frame4,yscrollcommand=scrollb2.set,height = 6)
            self.listbox2.grid(row=1, column = 0,sticky = W,columnspan=2,padx=15,ipadx=100)
            scrollb2.config(command=self.listbox2.yview)
            label13 = Label (self.frame4, text = "Users similar to you",fg = "white",bg = "blue4",font = ("Georgia",11))
            label13.grid(row = 0,column=2, sticky = W,padx=30,ipadx=10,pady=5)
            self.listbox3 = Listbox(self.frame4,height = 6)
            self.listbox3.grid(row=1, column = 2,sticky = W,padx=30,ipadx=70)
            self.listbox3.bind("<<ListboxSelect>>",self.display_info)
            label14 = Label (self.frame4, text = "User ratings (Select a user on the left)",fg = "white",bg = "brown4",font = ("Georgia",11))
            label14.grid(row = 0,column=3, sticky = W,pady=5,columnspan=2, )
            scrollb3 = Scrollbar(self.frame4)
            scrollb3.grid(row=1,column=6,ipady=25,sticky = W)
            self.listbox4 = Listbox(self.frame4,yscrollcommand=scrollb3.set,height = 6)
            self.listbox4.grid(row=1, column = 4,sticky = W,columnspan=2,ipadx=100)
            scrollb3.config(command=self.listbox4.yview)
            if similarity ==2:
                self.result_box(entryno,sim_pearson)
                self.user_based(entryno,sim_pearson)
            elif similarity == 3:
                self.result_box(entryno,sim_jaccard)
                self.user_based(entryno,sim_jaccard)
            else:
                self.result_box(entryno,sim_distance)
                self.user_based(entryno,sim_distance)
        else:                                          #to display item based results as well as recommendations
            self.frame4 = Frame(self)
            self.frame4.grid(row=5)
            label12 = Label (self.frame4, text = "Result Box (Recommendations):",fg = "yellow",bg = "black",font = (" ",11))
            label12.grid(row = 0,column=0, sticky = W,padx=15,pady=5,columnspan=2)
            scrollb2 = Scrollbar(self.frame4)
            scrollb2.grid(row=1,column=1,ipady=25,sticky = E)
            self.listbox2 = Listbox(self.frame4,yscrollcommand=scrollb2.set,height = 6)
            self.listbox2.grid(row=1, column = 0,sticky = W,columnspan=2,padx=15,ipadx=100)
            scrollb2.config(command=self.listbox2.yview)
            label13 = Label (self.frame4, text = "Foods you really liked",fg = "white",bg = "blue4",font = ("Georgia",11))
            label13.grid(row = 0,column=2, sticky = W,padx=30,ipadx=10,pady=5)
            self.listbox3 = Listbox(self.frame4,height = 6)
            self.listbox3.grid(row=1, column = 2,sticky = W,padx=30,ipadx=70)
            self.listbox3.bind("<<ListboxSelect>>",self.display_info)
            label14 = Label (self.frame4, text = "Similar tastes (Select a food on the left)",fg = "white",bg = "brown4",font = ("Georgia",11))
            label14.grid(row = 0,column=3, sticky = W,pady=5,columnspan=2, )
            scrollb3 = Scrollbar(self.frame4)
            scrollb3.grid(row=1,column=6,ipady=25,sticky = W)
            self.listbox4 = Listbox(self.frame4,yscrollcommand=scrollb3.set,height = 6)
            self.listbox4.grid(row=1, column = 4,sticky = W,columnspan=2,ipadx=100)
            scrollb3.config(command=self.listbox4.yview)
            if similarity == 2:
                self.result_box(entryno)
                self.item_based(entryno)
            elif similarity ==3:
                self.result_box(entryno,sim_jaccard)
                self.item_based(entryno,sim_jaccard)
            else:
                self.result_box(entryno,sim_distance)
                self.item_based(entryno,sim_distance)


    def user_based(self,entryno,algo):
        res = topMatches(all_users_dict,"user",entryno,algo)
        for t in res:                                            #formatting each element in this list of tuples for display
            edited = "%g ---> %s" %(round(t[0],2),t[1])
            self.listbox3.insert(END,edited)
    def item_based(self,entry,algo=sim_pearson):
        my_ratings = sorted(all_users_dict["user"].items(),key=lambda x:x[1],reverse=True) #sorting from descending order according to element in second index
        for item in my_ratings:
            edited = "%s ---> %g" %(item[0],item[1])
            self.listbox3.insert(END,edited)
    def result_box(self,entryno,algo=sim_pearson):
        self.listbox2.insert(0,"Similarity Score ---> Recommendation")
        resultbox = getRecommendations(all_users_dict,"user",algo)
        for result in resultbox[:entryno]:
            edited = "%g ---> %s" %(round(result[0],1),result[1])
            self.listbox2.insert(END,edited)


    def display_info(self,event=0,entryno=5):
        entryno = int(self.entry.get())
        if self.v1.get() == 1:
            self.listbox4.delete(0,END)
            currentselection = self.listbox3.curselection()
            active = self.listbox3.get(currentselection[0]).split(' ---> ')
            sahis = active[1]
            for item in all_users_dict.iteritems():
                if sahis == item[0]:
                    values = sorted(item[1].items(),key=lambda x:x[1],reverse=True) #sorting from descending order according to element in second index
                    self.listbox4.insert(0,"%s also rated the following:" %sahis)
                    for el in values[:entryno]:
                        ratings = "%s ---> %d" %(el[0],el[1])
                        self.listbox4.insert(END,ratings)
        else:   # for item based
            self.listbox4.delete(0,END)
            similarity = self.v2.get()
            if similarity ==1:
                algo = sim_distance
            elif similarity == 2:
                algo = sim_pearson
            else:
                algo = sim_jaccard
            currentselection = self.listbox3.curselection()
            active = self.listbox3.get(currentselection[0]).split(' ---> ')
            yemek = active[0]
            my_dict = {"user":all_users_dict["user"]}
            swap = transformPrefs(all_users_dict)
            #print swap
            #print yemek
            #print swap[yemek]
            similaritems = topMatches(swap,yemek,entryno,algo)
            print similaritems
            # for key in similaritems:
            #     if key == yemek:
            #         foodmatch = similaritems[yemek]
            self.listbox4.insert(0,"Foods similar to %s:" %yemek)
            # foodmatchstd =sorted(foodmatch,reverse=True)
            for els in similaritems:
                similarfood = "%g ---> %s" %(els[0],els[1])
                self.listbox4.insert(END,similarfood)
    def oldratings(self):
        db0 = anydbm.open("ownratings.db", "w")       #a database containing a dictionary of user, which also contains dictionary of items and their ratings, updated whenever user makes changes
        for key,vals in db0.items():
            pickleload = pickle.loads(vals)
        for fooditem,ratingpoint in pickleload.items():
            val = "%s ---> %d" %(fooditem,ratingpoint)
            self.listbox1.insert(END,val)
        db0.close()

def main():
    root = Tk()
    root.geometry("1024x768+100+10")
    app = Project_2(root)
    root.mainloop()
main()