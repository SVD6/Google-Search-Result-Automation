import tkinter
import sys
import datetime
import logging
import uuid
import tldextract
import time
import random
import xlsxwriter

from extract_emails import ExtractEmails
from google import standard_search
from tkinter import Label, Entry, StringVar, IntVar, Button, Frame, messagebox


# GLOBAL VARIABLES
city = ''
keywordPairs = []
badDomains = []
cities = []
target = 0
workbookName = ''


# START LOGGER
logging.basicConfig(filename='LOG ' + str(uuid.uuid1().hex) + '.txt', level=logging.DEBUG)
logging.info(str(datetime.datetime.now()) + ': Autobot started')


# Reset Function which runs at the start of every button click
def reset():
    global city, keywordPairs, workbookName, target
    city = None
    keywordPairs = []
    workbookName = None
    target = None


# Literally does everything else
def everythingelse():
    global keywordPairs, city, workbookName

    start_time = time.time()

    # MAKE THE WORKSHEET
    book = xlsxwriter.Workbook(workbookName + '.xlsx')
    wsh = book.add_worksheet()

    bold = book.add_format({'bold': 1})
    wsh.set_column(0, 2, 50)  
    wsh.write('A1', 'Contact Email', bold)
    wsh.write('B1', 'Website Link', bold)
    wsh.write('C1', 'Website Title', bold)

    # POPULATE KEYWORD PAIRS
    try:
        with open(fileName, 'r') as pairs:
            for line in pairs:
                final = line.rstrip('\n')
                word, num = final.split(',')
                keywordPairs.append((word, int(num)))
    except:
        logging.error(str(datetime.datetime.now()) + ': Error populating the keyword pairs')
        messagebox.showinfo('ERROR', 'Error populating keywordPairs: \n' + str(sys.exc_info()[0]))
        return 0
    # List of all domains visited
    domains = []
    # List of final excel entries
    exceltriples = []
    # List of emails
    gotemails = []
    # List of all links visited
    links = []
    # Current row of excel
    row = 1

    # PERFORM THE SEARCH AND EXTRACT THE EMAILS
    for word in keywordPairs:
        searchquery = str(city + " " + word[0])
        numresults = word[1]
        logging.info(str(datetime.datetime.now()) + 'Starting search for query: ' + searchquery)
        numsuccessful = 0
        firstpage = 1
        pagestosearch = int(((numresults - numsuccessful) / 10) + 1)

        while numsuccessful < numresults:
            for result in standard_search.search(query=searchquery, pages=pagestosearch, first_page=firstpage):
                if (numsuccessful == numresults):
                    pass
                else:
                    links.append(result.link)
                    domain = tldextract.extract(result.link)[1]

                    if (domain not in domains and domain not in badDomains):
                        print(domain)
                        domains.append(domain)
                        logging.info(str(datetime.datetime.now()) + 'Scraping URL: ' + str(result.link) + ' for emails')
                        em = ExtractEmails(url=result.link, depth=30, print_log=True, ssl_verify=True, user_agent='random')
                        emails = em.emails

                        if (len(emails) > 0):
                            numsuccessful += 1
                            logging.info(str(datetime.datetime.now()) + 'Found some emails, number:' + str(numsuccessful))

                            for email in emails:
                                if email not in gotemails:
                                    gotemails.append(email)
                                    exceltriples.append((result.link, email, result.name))
                                    wsh.write(row, 0, email)
                                    wsh.write(row, 1, result.link)
                                    wsh.write(row, 2, result.name)
                                    row += 1

            firstpage += pagestosearch
            pagestosearch = int(((numresults - numsuccessful) / 10) + 3)
            time.sleep(random.randint(5, 15))

        # for webURL in search(query=searchquery, tld='ca', start=130, pause=5.0, lang='en', tbs='0', safe='off', user_agent='random', 
        # num=10, stop=None, domains=None, only_standard=False, extra_params={}, tpe=''):
        #     logging.info(str(datetime.datetime.now()) + 'Scraping Result No.' + str(len(domains)) + ' URL: ' + webURL)
        #     domain = tldextract.extract(webURL)[1]
        #     if (domain not in domains and domain not in badDomains):
        #         domains.append(domain)
        #         logging.info(str(datetime.datetime.now()) + 'Scraping URL: ' + str(webURL) + ' for emails')
        #         em = ExtractEmails(webURL, True, 20, True, 'random').emails
        #         if (len(em) > 0):
        #             numlinks += 1
        #             links += 1
        #             print('Successful Domain no.' + str(links))
        #             for email in em:
        #                 if email not in gotemails:
        #                     gotemails.append(email)
        #                     excelpairs.append((webURL, email))
        #                     wsh.write(row, 0, email)
        #                     wsh.write(row, 1, webURL)
        #                     row += 1
            
        #     if (numlinks == numresults):
        #         break
    
    book.close()
    logging.info(str(datetime.datetime.now()) + ': Completed a search, here are the stats: \n' + 'Number of entries: ' + str(len(exceltriples)) + '\n' + 'Number of results searched: ' + str(len(links)) + '\n' + "\n Number of 'good' domains:" + str(len(domains)) + '\nNumber of domains with emails: ' + str(numsuccessful) + '\n' + 'Time Elapsed = ' + str((start_time - time.time())))
    messagebox.showinfo('SUCCESS', 'Search completed :D')


# Handles the button clicks
def buttonHandler(text, thiscity, filename):
    global city, keywordPairs, cities, workbookName
    reset()
    workbookName = text + '.txt'
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
