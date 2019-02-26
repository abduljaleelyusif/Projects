import ttk, tkFileDialog,tkMessageBox,anydbm,xlrd,pickle
db1 = anydbm.open("test.db","c")
d = {"u":{"a":3,"b":2,"c":1}}
p = pickle.dumps(d["u"])
db1["u"] = p
print db1
db1.close

db2 = anydbm.open("test.db","w")
d1 = {"a":1, "b":1}


for key,val in db2.items():
    l = pickle.loads(val)
    for m,n in d1.items():
        l[m] = l.get(m,0)+n
    rl = pickle.dumps(l)
    db2[key] = rl
print db2
print d1