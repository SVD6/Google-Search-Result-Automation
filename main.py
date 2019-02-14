import os
import tkinter
from tkinter import *
from query import 

root = tkinter.Tk()
root.height = 50
root.width= 50

def test():
    print('worked')

l = Label(root, text = "Enter your search query:", relief='flat')
l.grid(row=0, column=0, padx=10, pady=10)

searchquery = StringVar()
inp = Entry(root, textvariable=searchquery)
inp.grid(row=0, column=1, pady=10)

l = Label(root, text = "How many entries?", relief = 'flat')
l.grid(row=1, column=0, padx=10, pady=10) 

numresults = IntVar()
inp2 = Entry(root, textvariable=numresults)
inp2.grid(row=1, column=1, pady=10)

but = Button(root, text="Magic.", command= lambda: )
but.grid(row=2, column=0, pady=10)

root.mainloop()