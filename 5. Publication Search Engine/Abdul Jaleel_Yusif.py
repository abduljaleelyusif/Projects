from Tkinter import*
import ttk, tkFileDialog,tkMessageBox,re,urllib2,unicodedata,encodings,urllib,shelve,time
from bs4 import BeautifulSoup
from urllib2 import urlopen
from django.utils.encoding import smart_str


ignorewords = set(['the', 'of', 'to', 'and', 'a', 'in', 'is', 'it','for','are','so','an'])

dbtables = {'publist': 'publist.db', 'wordlocation':'wordlocation.db'}

links=[]
all_works=[]

class Project_5(Frame):
    def __init__(self, parent,dbtables):
        self.dbtables = dbtables
        Frame.__init__(self, parent)
        self.parent = parent
        self.frame1=Frame(self)
        self.frame1.pack(fill=X)
        self.frame1a=Frame(self.frame1)
        self.frame1a.pack(fill=X)
        self.frame1b=Frame(self.frame1)
        self.frame1b.pack(fill=X, pady=2,padx=240)
        self.frame1c=Frame(self.frame1)
        self.frame1c.pack(fill=X)

        self.frame2=Frame(self)
        self.frame2.pack(fill=X,pady=5,padx=250)
        self.frame2a=Frame(self.frame2)
        self.frame2a.pack(fill=X)
        self.frameb=Frame(self.frame2)
        self.frameb.pack(fill=X)
        self.frame2b=Frame(self.frameb)
        self.frame2b.pack(side=LEFT,fill=X)
        self.frame2ba=Frame(self.frame2b)
        self.frame2ba.pack(fill=X,pady=15)
        self.frame2bb=Frame(self.frame2b)
        self.frame2bb.pack(fill=X,pady=15)
        self.frame2c=Frame(self.frameb)
        self.frame2c.pack(side=LEFT,fill=X,padx=30)
        self.frame2d=Frame(self.frameb)
        self.frame2d.pack(side=LEFT,fill=X)

        self.frame3=Frame(self)
        self.frame3.pack(fill=X)
        self.frame3a=Frame(self.frame3)
        self.frame3a.pack(fill=X,anchor=W)
        self.frame3b=Frame(self.frame3)
        self.frame3b.pack(fill=X,anchor=W,padx=180)
        self.frame4=Frame(self.frame3)
        self.frame4.pack(anchor=E,padx=220)

        self.initUI()

    def __del__(self):
        self.close()

    def close(self):
        if hasattr(self, 'publist'): self.publist.close()
        if hasattr(self, 'wordlocation'): self.wordlocation.close()

    def initUI(self):
        self.parent.title("SEHIR Scholar")
        self.pack(fill=BOTH, expand = True)

        heading = Label (self.frame1a, text = "SEHIR Scholar", fg = "white", bg = "blue4",font = ("Georgia",18))
        heading.pack(fill=X)

        label1=Label(self.frame1b,font = ("Georgia",12),text = "Url for faculty list :")
        label1.pack(side=LEFT,fill=X, pady=2,padx=1)
        entryvar= StringVar()
        self.entry1=Entry(self.frame1b,font = (" ",12),textvariable=entryvar)
        self.entry1.pack(side=LEFT,fill=X,ipady=3,ipadx=100,pady=5,padx=2)
        entryvar.set("http://cs.sehir.edu.tr/en/people/")
        bi_button = ttk.Button(self.frame1b,text = "Build Index", command=self.build_index)
        bi_button.pack(side=LEFT,fill=X,padx=2,pady=2)

        self.entry2=Entry(self.frame1c, bg= 'white', fg='blue',font = (" ",12),width=60)
        self.entry2.pack(ipady=2,pady=3,anchor=CENTER)

        label2=Label(self.frame2a,font = ("Georgia",12,"bold"),text = "Ranking Criteria :")
        label2.pack(side=LEFT,fill=X, pady=2,anchor = NW)
        label3=Label(self.frame2a,font = ("Georgia",12,"bold"),text = "Weight :")
        label3.pack(side=LEFT,fill=X, pady=2,padx=40)
        label4=Label(self.frame2a,font = ("Georgia",12,"bold"),text = "Filter Papers :")
        label4.pack(side=LEFT,fill=X, pady=2)

        self.wf=IntVar()
        self.cb1 = Checkbutton(self.frame2ba, variable=self.wf)
        self.cb1.pack(side=LEFT,anchor = NW)
        label4=Label(self.frame2ba,font = ("Georgia",11),text = "Word Frequency :")
        label4.pack(side=LEFT,fill=X,anchor = NW)
        self.WF_weight=Entry(self.frame2ba,width=5)
        self.WF_weight.pack(side=LEFT,ipady=2,padx=45,anchor = NE)

        self.cc=IntVar()
        self.cb2 = Checkbutton(self.frame2bb, variable=self.cc)
        self.cb2.pack(side=LEFT,anchor = NW,pady=2)
        label5=Label(self.frame2bb,font = ("Georgia",11),text = "   Citation Count :")
        label5.pack(side=LEFT,fill=X,anchor = NW)
        self.CC_weight=Entry(self.frame2bb,width=5)
        self.CC_weight.pack(side=LEFT,ipady=2,padx=45,anchor = NE)

        self.listbox1= Listbox(self.frame2c, height=5,width=35,bd=2,selectmode=EXTENDED)
        self.listbox1.pack(fill=X)
        scroll_bar1= ttk.Scrollbar(self.frame2c,orient = HORIZONTAL)
        scroll_bar1.pack(anchor=E,fill=X,ipadx=18)
        scroll_bar1.config(command=self.listbox1.xview)
        search_button = ttk.Button(self.frame2d,text = "Search", command = self.search_results)
        search_button.pack(anchor=NE)

        self.searchres=Label(self.frame3a,font = ("Helvetica",12),fg="red",text = " n Publications (m seconds) :")
        self.searchres.pack(anchor = W,padx=200)
        self.text= Text(self.frame3b,width=100,height=16,bg= 'white',font=('', 10),exportselection=0)
        self.text.pack(side=LEFT,pady=5,anchor=W)
        scroll_bar2= ttk.Scrollbar(self.frame3b)
        scroll_bar2.pack(side=LEFT,fill=Y)
        scroll_bar2.config(command=self.text.yview)
        label6=Label(self.frame4,text = "Page:")
        label6.pack(side=LEFT)
        prevb = ttk.Button(self.frame4, text = "Previous",command = self.previous_button)
        prevb.pack(side=LEFT,padx=3)
        self.label7=Label(self.frame4,text = "no.",relief=RAISED,fg='white',bg='blue')
        self.label7.pack(side=LEFT)
        nextb = ttk.Button(self.frame4, text = "Next", command = self.next_button)
        nextb.pack(side=LEFT,padx=3)

    def build_index(self):
        self.createindextables()
        url = self.entry1.get() #gets the url from entry widget, default is the website for this project
        soup = BeautifulSoup(urllib2.urlopen(url).read(),"html.parser")
        all_links = soup.find_all("a")  #link for all lecturers

        baselink= "http://cs.sehir.edu.tr"
        for link in all_links:
            link_ad = baselink + str(link.get("href"))
            if "profile" in link_ad and link_ad not in links:   #avoiding page links that are not related to this project
                links.append(link_ad)
        for l in links:
            soup1 = BeautifulSoup(urllib2.urlopen(l).read(),"html.parser")
            works = soup1.find_all("div", {"class":"tab-pane active pubs"})  #class containing list of projects for each lecturer
            for w in works:
                wrk = w.text
                work = re.split(r"\s{5}\d{1,3}\.",wrk)       #splitting individual projects
                work_per_person=[]
                for eser in work:
                    conv = eser.replace("\n","").replace("      ","").encode("utf-8")
                    if  conv !='' and "a" in conv:
                        work_per_person.append(conv)
                all_works.append(work_per_person)

        #collecting citation value for each work
        #setting location for words and how many times they appear in location
        for person in all_works:
            for wrk in person:
                ss= wrk.split(" ")
                for i in range(len(ss)):
                    if "Citations]" in ss[i]:
                        n = ss[i-4].replace("[","")
                        c_rank = float(n)
                        break
                    elif "Citation]" in ss[i]:
                        c_rank = 1.0
                        break
                    elif "Citations]" not in ss[i] or "Citation]" not in ss[i] :    #default ranking for projects that have not citations
                        c_rank = 0.0
                self.publist[wrk] = c_rank
                self.addtoindex(wrk)
        groups = ["Book Chapters","Conference-Works","Journal Papers","Patents"]    #populating listbox
        for el in groups:
            self.listbox1.insert(END,el)
        self.listbox1.selection_anchor(0)
        self.listbox1.select_set(ANCHOR,END)

    def addtoindex(self, pub):
        # Get the individual words
        words = self.separatewords(pub)
        # Record each word found in this pub
        for i in range(len(words)):
            word = smart_str(words[i])
            if word in ignorewords:
                continue

            self.wordlocation.setdefault(word, {})
            self.wordlocation[word].setdefault(pub, 0)
            self.wordlocation[word][pub] +=1

        return True

    def separatewords(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    def createindextables(self):
        # {pub:citation}
        self.publist = shelve.open(self.dbtables['publist'], writeback=True, flag='c')

        #{word:{pub: appearance val}}
        self.wordlocation = shelve.open(self.dbtables['wordlocation'], writeback=True, flag='c')

    def settings_check(self):
        selecteditems =self.listbox1.curselection()     #list of selected paper type
        self.selectedlist=[]
        for i in selecteditems:
            self.selectedlist.append(self.listbox1.get(i))

        #getting keywords
        self.kwords = self.entry2.get()

        #checking ranking critetia
        self.wfreq = self.wf.get()
        self.ccount = self.cc.get()
        #getting criteria weight
        self.wf_w = self.WF_weight.get()
        self.cc_w = self.CC_weight.get()

        #error handlers
        if self.kwords == "":
            return tkMessageBox.showinfo("Error!", "Please provide at least one keyword")
        if self.wfreq == 0 and self.ccount == 0:
            return tkMessageBox.showinfo("Error!", "Please choose at least one ranking measure")
        if self.wfreq ==1 and self.ccount ==1:
            if self.wf_w == "" or self.cc_w == "":
                return tkMessageBox.showinfo("Error!", "Please provide weights if multiple ranking measure is selected")
        if len(self.selectedlist) ==0:
            return tkMessageBox.showinfo("Error!", "Please choose at least one paper category")

    def search_results(self):
        try:
            self.i=0
            self.start = time.time()
            self.settings_check()
            self.rankedscores = self.query(self.kwords)
            if len(self.rankedscores)==0:
                return tkMessageBox.showinfo("Error!", 'No results found!')
            self.write_text(self.i)
            totalpubs = len(self.rankedscores)
            end = time.time()
            elapsed = round((end - self.start),2)
            self.searchres.config(text= "%d Publications(%02.2f seconds)" % (totalpubs,elapsed))
        except ValueError:
            pass

    def write_text(self,page):   #writing works in the Text widget
        if page >= 0:
            self.text.delete("1.0",END)
        rankedscores = self.rankedscores
        collect =[]
        counter=1
        for (score,work) in rankedscores:
            res = str(counter) + ". " + work
            vals = "%f"%(score)
            collect.append((res,vals))
            counter+=1
        #page division is done by creating sublist (containing 10 works) of the result list
        pagedivision = [collect[10*i:10*(i+1)] for i in range(len(collect)/10 + 1)]
        self.pages = [pd for pd in pagedivision if len(pd)>0]  #this is to avoid appending empty lists (also avoids writing empty pages on Text widget)
        scores_pp=[]
        for eser,score in self.pages[page]:
            self.text.insert(END,eser + "   " + score + "\n\n")
            scores_pp.append(score)

        keywords = self.kwords.split(" ")    #highlighting scores of works
        for sc in scores_pp:
            self.highlight(sc,"red")

        for kw in keywords:                  #highlighting keywords used for searching
            self.highlight(kw,"blue")

        self.label7.config(text = "%s" % (page+1))
    def next_button(self):
        self.i+=1
        if self.i > len(self.pages)-1:       #deactivates next button after printing all pages
            self.i -=1
            return

        self.write_text(self.i)
    def previous_button(self):
        self.i-=1
        if self.i < 0:                      #deactivates previous button when current page is 1
            self.i = 0
            return
        self.write_text(self.i)

    def getmatchingpubs(self,q):
        results = {}
        # splitting words
        words = [smart_str(word) for word in q.split()]
        if words[0] not in self.wordlocation:
                return results, words

        pub_set = set(self.wordlocation[words[0]].keys())

        for word in words[1:]:
            if word not in self.wordlocation:
                return results, words
            pub_set = pub_set.intersection(self.wordlocation[word].keys())

        for paper in pub_set:
            results[paper] = []
            for word in words:
                results[paper].append(self.wordlocation[word][paper])

        return results, words
    def getscoredlist(self, results, wordfreq,citationfreq,wfweight=1,ccweight=1):
        totalscores = dict([(paper, 0) for paper in results])

        def normalizescores(scores,smallIsBetter=0):
            vsmall = 0.00001 # Avoid division by zero errors
            if smallIsBetter:
                minscore=min(scores.values())
                minscore=max(minscore, vsmall)
                return dict([(u,float(minscore)/max(vsmall,l)) for (u,l) \
                             in scores.items()])
            else:
                maxscore = max(scores.values())
                if maxscore == 0:
                    maxscore = vsmall
                return dict([(u,float(c)/maxscore) for (u,c) in scores.items()])

        #getting word frequency per publication
        def frequencyscore(results):
            counts = {}
            for paper in results:
                score = 1
                for appearance in results[paper]:
                    score *= appearance
                counts[paper] = score
            return normalizescores(counts, smallIsBetter=False)

        # getting citation values
        def citationscore(results):
            citations = {}
            for paper in results:
                for pub in self.publist:
                    if paper == pub:
                        score = self.publist[pub]
                citations[paper] = score
            return normalizescores(citations, smallIsBetter=False)

        # word frequency scoring according to ranking criteria
        if wordfreq == 1 and citationfreq == 1:
            weights = [(wfweight, frequencyscore(results)),
                       (ccweight, citationscore(results))]
        elif wordfreq == 1 and citationfreq == 0:
            weights = [(wfweight, frequencyscore(results))]
        elif wordfreq == 0 and citationfreq == 1:
            weights = [(ccweight, citationscore(results))]

        for (weight,scores) in weights:
            for paper in totalscores:
                totalscores[paper] += weight*scores.get(paper, 0)

        return totalscores

    def query(self,q):
        results, words = self.getmatchingpubs(q)
        if len(results) == 0:
            return tkMessageBox.showinfo("Error!", 'No matching pages found!')
        if self.wf_w == "":
            self.wf_w = 1
        if self.cc_w == "":
            self.cc_w = 1

        scores = self.getscoredlist(results,int(self.wfreq),int(self.ccount),int(self.wf_w),int(self.cc_w))
        rankedscores = sorted([(score,work) for (work,score) in scores.items()],reverse=1)
        if len(self.selectedlist) ==4:      #results for all categories
            return rankedscores
        else:
            special = self.filtering(self.selectedlist,rankedscores)   #filtering out selected category
            return sorted(special,reverse=1)

    def filtering(self,flist,rscores):  #"Book Chapters","Conference-Works","Journal Papers","Patents"
        filtered = []
        for f in flist:
            if f == "Journal Papers":
                journal = ["J. Sch","IJ","J. Bio","B J.","t. J.","B J.","J. Vis","J Pro","Journal"]
                for i in journal:
                    for score,work in rscores:
                        if i in work and (score,work) not in filtered:
                            filtered.append((score,work))
            elif f == "Patents":
                for score,work in rscores:
                    if "Patent" in work  and (score,work) not in filtered:
                        filtered.append((score,work))
            elif f == "Conference-Works":
                for score,work in rscores:
                    if "Conference" in work and (score,work) not in filtered:
                        filtered.append((score,work))
            else:
                for score,work in rscores:
                    if "Patent" not in work  and "Conference" not in work:
                        if (score,work) not in filtered:
                            filtered.append((score,work))
        return filtered

    def highlight(self, seq,col): #source: https://bytes.com/topic/python/answers/932512-how-highlight-text-tkinter-do-you-know-what-i-am-doing-wrong
        h = seq                   #modified for usage in this project
        i = len(seq)
        idx = "1.0"
        while True:
            idx = self.text.search(seq, idx, nocase=1, stopindex='end')
            if idx:
                idx2 = self.text.index("%s+%dc" % (idx, i))
                self.text.tag_add(h, idx, idx2)
                self.text.tag_config(h, foreground=col)
                idx = idx2
            else: return

    def opendb(self):
        # {pub:citation}
        self.publist = shelve.open(self.dbtables['publist'], flag='r')
        #{word:{pub: appearance val}}
        self.wordlocation = shelve.open(self.dbtables['wordlocation'], flag='r')

def main():
    root = Tk()
    root.geometry("1100x600+120+20")
    app = Project_5(root,dbtables)
    root.mainloop()
main()