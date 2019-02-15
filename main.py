import tldextract

try:
    import os
    import tkinter
    import xlsxwriter
    import extractEmails
    
    from googlesearch import search 
    from tkinter import Label, Entry, StringVar, IntVar, Button, Frame
except ImportError:
    print("Error importing a module")

def buttonHandler(searchquery, numresults, filename):
    book = xlsxwriter.Workbook(filename + '.xlsx')
    wsh = book.add_worksheet()

    bold = book.add_format({'bold': 1})
    wsh.set_column(0, 2, 30)  
    wsh.write('A1', 'Website Title', bold)
    wsh.write('B1', 'Website Link', bold)
    wsh.write('C1', 'Contact Email', bold)

    links = runQuery(searchquery, numresults)
    emailExtract(links, book)

    book.close()

def runQuery(searchquery, numresults):

    urls = []
    links = []
    stop = 0

    for webURL in search(searchquery, tld='ca', safe='off', start=0, pause=2):

        if (stop == (numresults + 1)):
            break 

        extraction = tldextract.extract(webURL)
        domain = extraction.domain()

        if (domain not in urls and domain != 'www.airbnb.com' and domain != 'www.facebook.com' and domain != 'www.tripadvisor.com' and domain != 'www.kayak.com' 
        and domain != 'www.expedia.com' and domain != 'www.viator.com' and domain != 'www.getyourguide.com' and domain != 'www.youtube.com' and domain != 'www.amazon.com'):
            print(domain)
            urls.append(domain)
            links.append(webURL)
        
        stop += 1
    return links

def emailExtract(links, excelsheet):
    
    for url in links:
        return
    return

root = tkinter.Tk()
root.height = 50
root.width= 50

root.title("Wandure Autobot")

l = Label(root, text = "Enter your search query:", relief='flat')
l.grid(row=0, column=0, padx=5, pady=10)

searchQuery = StringVar()
inp = Entry(root, textvariable=searchQuery)
inp.grid(row=0, column=1, padx=10, pady=10)

l = Label(root, text = "How many entries?", relief = 'flat')
l.grid(row=1, column=0, padx=5, pady=10) 

numResults = IntVar()
inp2 = Entry(root, textvariable=numResults)
inp2.grid(row=1, column=1, padx=10, pady=10)

l = Label(root, text = "Name of Excel File:", relief='flat')
l.grid(row=2, column=0, padx=5, pady=10)

fileName = StringVar()
inp3 = Entry(root, textvariable=fileName)
inp3.grid(row=2, column=1, padx=10, pady=10)

but = Button(root, text="Magic", command= lambda: buttonHandler(inp.get(), inp2.get(), inp3.get()))
but.grid(row=3, column=0, pady=10)

root.resizable(False, False)

root.mainloop()
