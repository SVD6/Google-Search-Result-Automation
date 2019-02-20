import tldextract
import os
import tkinter
import xlsxwriter
import re
import requests
import urllib3
import sys

from googlesearch import search 
from lxml import html
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from tkinter import Label, Entry, StringVar, IntVar, Button, Frame

# Disable InsecureRequestWarning, makes the logs cleaner
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Initialize some global variables
ua = UserAgent()
agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
            'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
            'safari': ua.safari, 'random': ua.random}

bad_domains = ['airbnb', 'youtube', 'facebook', 'viator', 'expedia', 'tripadvisor', 'kayak', 'amazon', 
            'likealocalguide', 'getyourguide', 'wikipedia', 'twitter', 'bloomberg']

for_scan = []
scanned = []
emails = []
excel_ready = []
depth = 50
print_log = True
verify = False
finalnum = 0
urls = []


# Handler for the "Magic" Button
def buttonHandler(searchquery, numresults, filename):
    global for_scan, finalnum, excel_ready
    # if (os.path.isfile('./' + filename + '.txt'))
    # Create the workbook and format the first
    book = xlsxwriter.Workbook(filename + '.xlsx')
    wsh = book.add_worksheet()

    bold = book.add_format({'bold': 1})
    wsh.set_column(0, 2, 50)  
    wsh.write('A1', 'Website Title', bold)
    wsh.write('B1', 'Website Link', bold)
    wsh.write('C1', 'Contact Email', bold)

    # Perform the search and collect a list of links
    tosearchlinks = runQuery(searchquery, numresults)

    # Use the email extractor for each URL and all sub-URL's
    for url in tosearchlinks:
        emailExtract(url)
    
    print(finalnum)
    # Take all the url-email pairs and put them in the excel file
    row = 1
    for pair in excel_ready:
        print(pair[0] + pair[1])
        wsh.write(row, 0, pair[2], None)
        wsh.write(row, 1, pair[0], None)
        wsh.write(row, 2, pair[1], None)
        row += 1
    book.close()

# Runs the search query on the given paramaters
def runQuery(searchquery, numresults):
    global urls
    links = []
    stop = 0

    for webURL in search(searchquery, tld='ca', safe='off', start=len(urls), pause=5):
        if (stop == (numresults)):
            break 

        extraction = tldextract.extract(webURL)
        domain = extraction[1]

        if (domain not in urls and domain not in bad_domains):
            print(domain)
            urls.append(domain)
            links.append(webURL)
            stop += 1
    return links

# Sub-link + email extractor
def emailExtract(url):
    global depth, agents, finalnum, for_scan, scanned, print_log
    depth = 30
    headers = {'User-Agent': agents['chrome']}
    try:
        r = requests.get(url, headers = headers, verify = verify)
        scanned.append(url)
        if r.status_code == 200:
            get_all_links(url, r.text)
            email_result = get_emails(url, r.text)
            if (email_result == 1):
                global finalnum
                finalnum += 1
    except:
        print('Error @ Line 93 ',sys.exc_info()[0])
    if print_log:
        print_logs()
    for new_url in for_scan[:depth]:
        if new_url not in scanned:
            emailExtract(new_url)

# Print the state of the current url/email
def print_logs():
    global emails, scanned
    print('URLs: {}, emails: {}'
            .format(len(scanned), len(emails)))

# Given one URL and an html page, find all sub-links based on the depth number
def get_all_links(url, page):
    global for_scan
    try:
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
            except:
                print('Error ',sys.exc_info()[0])
    except:
        print('Error @ Line 111',sys.exc_info()[0])

# Given a URL and it's corresponding text, find all emails on the page
def get_emails(url, page):
    global emails, urls
    result = 0
    extraction = tldextract.extract(url)
    domain = extraction[1]
    t_emails = re.findall(r'\b[\w.-]+?@\w+?\.(?!jpg|png|jpeg)\w+?\b', page)
    if t_emails:
        print(len(t_emails))
        for email in t_emails:
            if email not in emails:
                soup = BeautifulSoup(page)
                emails.append(email)
                excel_ready.append((url, email, str(soup.title.contents[0])))

            if (email not in emails and domain not in urls):
                result = 1
    return result

# BUILD THE UI
root = tkinter.Tk()
root.height = 50
root.width= 50

root.title('Wandure Autobot')

l = Label(root, text = 'Enter your search query:', relief='flat')
l.grid(row=0, column=0, padx=5, pady=10)

searchQuery = StringVar()
inp = Entry(root, textvariable=searchQuery)
inp.grid(row=0, column=1, padx=10, pady=10)

l = Label(root, text = 'How many entries?', relief = 'flat')
l.grid(row=1, column=0, padx=5, pady=10) 

numResults = IntVar()
inp2 = Entry(root, textvariable=numResults)
inp2.grid(row=1, column=1, padx=10, pady=10)

l = Label(root, text = 'Name of Excel File:', relief='flat')
l.grid(row=2, column=0, padx=5, pady=10)

fileName = StringVar()
inp3 = Entry(root, textvariable=fileName)
inp3.grid(row=2, column=1, padx=10, pady=10)

but = Button(root, text='Magic', command= lambda: buttonHandler(inp.get(), int(inp2.get()), inp3.get()))
but.grid(row=3, column=0, pady=10)

root.resizable(False, False)

root.mainloop()
