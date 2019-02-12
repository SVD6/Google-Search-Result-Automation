import xlsxwriter
import urllib
import os
import tkinter
from tkinter import *

try: 
    from googlesearch import search 
except ImportError:  
    print("No module named 'google' found") 

os.remove('Test1.xlsx')

def googleSearch(query, results):
    urls = []
    links = []

    for j in search(query, tld='ca', safe='off', start=0, stop=results, pause=2):
        a, b, c, d = j.split('/', 3)

        if (c not in urls and c != 'www.airbnb.com' and c != 'www.facebook.com' and c != 'www.tripadvisor.com'):
            print(c)
            urls.append(c)
            links.append(j)
    return links

def findEmails():
    return

def setupSheet(filename):
    book = xlsxwriter.Workbook(filename + '.xlsx')
    wsh = book.add_worksheet()

    bold = book.add_format({'bold': 1})
    wsh.set_column(0, 2, 30)

    wsh.write('A1', 'Website Title', bold)
    wsh.write('B1', 'Website Link', bold)
    wsh.write('C1', 'Contact Email', bold)
    book.close()

def printtest():
    print('sup nigga')

setupSheet('Test1')     
# googleSearch('Sai Vikranth Desu', 10)

root = tkinter.Tk()
root.height = 50
root.width= 50

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

but = Button(root, text="Magic.")
but.grid(row=2, column=0, pady=10)

root.mainloop()