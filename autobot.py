import tkinter
import sys
import datetime
import logging
import uuid

from extract_emails import ExtractEmails
from googlesearch import search 
from tkinter import Label, Entry, StringVar, IntVar, Button, Frame, messagebox

# GLOBAL VARIABLES
city = ''
fileName = ''
keywordPairs = []
bad_domains = []
cities = []
target = 0

# START LOGGER
logging.basicConfig(filename='LOG ' + str(uuid.uuid1().hex) + '.txt', level=logging.DEBUG)
logging.info(str(datetime.datetime.now()) + ': Autobot started')

# Reset Function which runs at the start of every button click
def reset():
    global city, keywordPairs, fileName, target
    city = None
    keywordPairs = None
    fileName = None
    target = None

# Literally does everything else
def everythingelse():
    global keywordPairs, city, fileName

    # POPULATE KEYWORD PAIRS
    try:
        with open(fileName, 'r') as pairs:
            for line in pairs:
                final = line.rstrip('\n')
                word, num = final.split(',')
                keywordPairs.append((word, int(num)))
    except:
        messagebox.showinfo('ERROR', 'Error populating keywordPairs: \n' + str(sys.exc_info()[0]))
        return 0

    for word in keywordPairs:
        print(city + " " + word[0])
    
    for keyword in keywordPairs:
        target = keyword[1]
        print(target)

# Handles the button clicks
def buttonHandler(text, thiscity, three):
    global city, keywordPairs, fileName, cities
    reset()
    fileName = text + '.txt'

    # VERIFY CITY
    try:
        with open('cities.txt', 'r') as lines:
            for line in lines:
                final = line.rstrip('\n')
                cities.append(final)
    except:
        messagebox.showinfo('ERROR', 'Error verifying city: \n' + str(sys.exc_info()[0]))
        return None
    
    print(cities)
    
    if (thiscity not in cities):
        messagebox.showinfo('WARNING', "That's not a valid city, please try again.")
        return None
    else:
        city = thiscity
    
    # POPULATE BAD DOMAINS
    try:
        with open('baddomains.txt', 'r') as lines2:
            for line2 in lines2:
                final2 = line2.rstrip('\n')
                bad_domains.append(final2)
    except:
        messagebox.showinfo('ERROR', 'Error filling bad domains list: \n' + str(sys.exc_info()[0]))
    
    result = everythingelse()

    # ALLOWS THE TOOL TO BE RUN MULTIPLE TIMES IN THE SAME INSTANCE
    if (result != None):
        messagebox.showinfo('FAILED', 'Failed to run tool, try again')

# BUILD THE UI
root = tkinter.Tk()
root.height = 50
root.width= 50

root.title('Wandure Autobot')

l = Label(root, text = 'Keyword textfile:', relief='flat')
l.grid(row=0, column=0, padx=5, pady=10)

keywordFile = StringVar()
inp = Entry(root, textvariable = keywordFile)
keywordFile.set('keywords')
inp.grid(row=0, column=1, padx=10, pady=10)

l = Label(root, text = 'City Name:', relief = 'flat')
l.grid(row=1, column=0, padx=5, pady=10) 

cityName = StringVar()
inp2 = Entry(root, textvariable = cityName)
inp2.grid(row=1, column=1, padx=10, pady=10)

l = Label(root, text = 'Name of Excel File:', relief='flat')
l.grid(row=2, column=0, padx=5, pady=10)

fileName = StringVar()
inp3 = Entry(root, textvariable=fileName)
inp3.grid(row=2, column=1, padx=10, pady=10)

but = Button(root, text='Magic', command= lambda: buttonHandler(inp.get(), inp2.get(), inp3.get()))
but.grid(row=3, column=0, pady=10)

root.resizable(False, False)

root.mainloop()

# em = ExtractEmails('https://www.madridcitytours.com/', True, 20, True, 'chrome')
# emails = em.emails
# print (emails)
# print (len(em.for_scan))