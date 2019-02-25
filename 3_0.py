import tkinter
import logging
import sys
import uuid
import time
import random
import selenium
import xlsxwriter
import selenium
import tldextract
import datetime

from tkinter import Label, Entry, StringVar, IntVar, Button, Frame, messagebox
from selenium import webdriver
from extract_emails import ExtractEmails
from bs4 import BeautifulSoup

# GLOBAL VARIABLES
city = ''
workbookName = ''
wordsfile = ''
keywordPairs = []
badDomains = []
cities = []
target = 0
emails = []
language = 'en'
perpage = 50
domains = []
numsuccessful = 0

#Initiate stuff
driver = webdriver.Chrome('C:/Users/sai.vikranth/Documents/autobot/Google-Search-Result-Automation/Archive/chromedriver.exe')
NoSuchElementException = selenium.common.exceptions.NoSuchElementException
logging.basicConfig(filename='LOG ' + str(uuid.uuid1().hex) + '.txt', level=logging.DEBUG)
logging.info(str(datetime.datetime.now()) + ': Autobot started')

# Reset Function which runs at the start of every button click
def reset():
    global city, keywordPairs, workbookName, target
    city = None
    keywordPairs = []
    workbookName = None
    target = None

def everythingelse():
    global workbookName, emails, city, keywordPairs, language, perpage, driver, domains, numsuccessful, wordsfile
    start_time = time.time()

    # MAKE THE WORKSHEET
    book = xlsxwriter.Workbook(workbookName + '.xlsx')
    wsh = book.add_worksheet()

    bold = book.add_format({'bold': 1})
    wsh.set_column(0, 2, 50)  
    wsh.write('A1', 'Contact Email', bold)
    wsh.write('B1', 'Website Link', bold)
    wsh.write('C1', 'Website Title', bold)
    row = 1
    exceltriples = []

    # POPULATE KEYWORD PAIRS
    try:
        with open(wordsfile, 'r') as pairs:
            for line in pairs:
                final = line.rstrip('\n')
                word, num = final.split(',')
                keywordPairs.append((word, int(num)))
    except:
        logging.error(str(datetime.datetime.now()) + ': Error populating the keyword pairs')
        messagebox.showinfo('ERROR', 'Error populating keywordPairs: \n' + str(sys.exc_info()[0]))
        return 0

    for word in keywordPairs:
        searchquery = str(city + "+" + word[0])
        logging.info(str(datetime.datetime.now()) + ': Started searching for ' + searchquery)
        isActive = True
        start = 0
        currlinks = []
        while isActive:
            url = 'https://www.google.com/search?nl=' + language + '&q=' + searchquery + '&start=' + str(start) + '&num=' + str(perpage)
            driver.get(url)
            try:
                driver.find_element_by_class_name("g")
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                divs = soup.findAll("div", attrs={"class": "g"})
                for div in divs:
                    a = div.find("a")
                    link = a["href"]
                    domain = tldextract.extract(link)[1]
                    if (domain not in domains and domain not in badDomains):
                        domains.append(link)
                        currlinks.append(link)
            except NoSuchElementException:
                print('No searchresults here')
                logging.error(str(datetime.datetime.now()) + ': No more search results left')
                isActive = False
                continue
            except Exception:
                print('Error finding search divs')
                logging.error(str(datetime.datetime.now()) + ': Some other error occurred during search')
                continue

            start += perpage
            time.sleep(random.randint(10, 15))
        
        logging.info(str(datetime.datetime.now()) + ': Completed searching for ' + searchquery)
        logging.info(str(datetime.datetime.now()) + ': Started email scraping for ' + searchquery)

        driver.close()
        print(len(currlinks))
        for url in currlinks:
            em = ExtractEmails(url=url, depth=30, print_log=True, ssl_verify=True, user_agent='random')
            deseemails = em.emails
            if (len(deseemails) > 0):
                numsuccessful += 1
                for email in deseemails:
                    if email not in emails:
                        emails.append(email)
                        exceltriples.append((url, email))
                        wsh.write(row, 0, email)
                        wsh.write(row, 1, url)
                        row += 1
            
            if (len(emails) == 5):
                break

    book.close()
    logging.info(str(datetime.datetime.now()) + ': Completed a search, here are the stats: \n' + 'Number of entries: ' + str(len(exceltriples)) + '\n' + 'Number of results searched: ' + str(len(domains)) + '\n' + "\n Number of 'good' domains:" + str(len(domains)) + '\nNumber of domains with emails: ' + str(numsuccessful) + '\n' + 'Time Elapsed = ' + str((start_time - time.time())))
    messagebox.showinfo('SUCCESS', 'Search completed :D')

# Handles the button clicks
def buttonHandler(text, thiscity, filename):
    global city, keywordPairs, cities, workbookName, wordsfile
    reset()
    workbookName = filename + '.txt'
    wordsfile = text + '.txt'
    logging.info(str(datetime.datetime.now()) + ': Magic Button Pressed')

    # VERIFY CITY
    try:
        with open('cities.txt', 'r') as lines:
            for line in lines:
                final = line.rstrip('\n')
                cities.append(final)
    except:
        messagebox.showinfo('ERROR', 'Error verifying city: \n' + str(sys.exc_info()[0]))
        return None
    
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
                badDomains.append(final2)
    except:
        messagebox.showinfo('ERROR', 'Error filling bad domains list: \n' + str(sys.exc_info()[0]))
    
    result = everythingelse()

    # ALLOWS THE TOOL TO BE RUN MULTIPLE TIMES IN THE SAME INSTANCE
    if (result != None):
        messagebox.showinfo('FAILED', 'Failed to run tool, try again')

# Simply shuts down the tool
def doneHandler():
    logging.info(str(datetime.datetime.now()) + ': Autobot ended')
    driver.quit()
    sys.exit()


# BUILD THE UI
root = tkinter.Tk()
root.height = 50
root.width= 50

root.title('Wandure Autobot')

l = Label(root, text = 'Keyword File:', relief='flat')
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

but = Button(root, text='Search', command= lambda: buttonHandler(inp.get(), inp2.get(), inp3.get()))
but.grid(row=3, column=0, pady=10)

but = Button(root, text='Finish', command= lambda: doneHandler())
but.grid(row=3, column=1, pady=10)

root.resizable(False, False)
root.mainloop()