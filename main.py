import tldextract

import os
import tkinter
import xlsxwriter
import re
import requests
import urllib3

from googlesearch import search 
from lxml import html
from fake_useragent import UserAgent
from tkinter import Label, Entry, StringVar, IntVar, Button, Frame

ua = UserAgent()
agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
              'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
              'safari': ua.safari, 'random': ua.random}
for_scan = []
scanned = []
emails = []
depth = 20

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
        domain = extraction[1]

        if (domain not in urls and domain != 'airbnb' and domain != 'facebook' and domain != 'tripadvisor' and domain != 'kayak' 
        and domain != 'expedia' and domain != 'viator' and domain != 'getyourguide' and domain != 'youtube' and domain != 'amazon'):
            print(domain)
            urls.append(domain)
            links.append(webURL)
            stop += 1
    return links

def emailExtract(links, excelsheet):
    verify = False
    headers = {'User-Agent': agents['chrome']}
    
    for url in links:
        r = requests.get(url, headers = headers, verify = verify)
        scanned.append(url)
        if r.status_code == 200:
            get_all_links(url, r.text)
            get_emails(r.text)

    return

def get_all_links(url, page):
        tree = html.fromstring(page)
        all_links = tree.findall('.//a')
        for link in all_links:
            try:
                link_href = link.attrib['href']
                if link_href.startswith(url) or link_href.startswith('/'):
                    if link_href.startswith('/'):
                        link_href = url + link_href
                    if link_href not in for_scan:
                        for_scan.append(link_href)
            except KeyError:
                pass

def get_emails(self, page):
        num = 0
        emails = re.findall(r'\b[\w.-]+?@\w+?\.(?!jpg|png|jpeg)\w+?\b', page)
        if emails:
            for email in emails:
                if email not in self.emails:
                    self.emails.append(email)

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

but = Button(root, text="Magic", command= lambda: buttonHandler(inp.get(), int(inp2.get()), inp3.get()))
but.grid(row=3, column=0, pady=10)

root.resizable(False, False)

root.mainloop()
