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
wordsFile = ''
keywordPairs = []
badDomains = []
cities = []
target = 0
emails = []
language = 'en'
perPage = 50
domains = []
numSuccessful = 0
numResults = 0
links = ['aporras@julia.net', 'incoming@julia.net', 'service@tours4fun.com', 'tour@corp.realmadrid', 'info@madridmuseumtours.com', 'webmaster@civitatis.com', 'rick@ricksteves.com', 'info@rivieratravel.co', 'groups@rivieratravel.co', 'atencionalcliente@busvision.net', 'info@busvision.net', 'info.neworleansbus@gmail.com', 'customerservices@panchotours.com', 'slick@1.8', 'info@walksofitaly.com', 'info@madridurbanadventures.com', 'info@madride.net', 'nfo@insidersmadrid.com', 'info@insidersmadrid.com', 'jetsettingfools@outlook.com', 'info@ogotours.com', 'Emailinfo@devourtours.comPhoneSpain', 'webmaster@toursgratis.com', 'info@toursgratis.com', 'visitas@grupobme.es', 'tour@atleticodemadrid.com', 'comunicacion@clubatleticodemadrid.com', 'info@boostespana.com', 'newmadridmail@gmail.com',
'madrid@trixi.com', 'info@madridbiketours.com', 'info@rainbowgaytours.com', 'info@bravobike.com', 'enquiries@globusfamily.co', 'info@bajabikes.eu', 'username@example.com', 'info@nattivus.com', 'info@madrides.es', 'info@accessiblemadrid.com', 'contact@rentandroll.es', 'lisboa@localtuktuk.com', 'madrid@localtuktuk.com', 'info@citylifemadrid.com', 'tarjetatransportepublico@crtm.es', 'atencion.visitante@museodelprado.es', 'normalize@6.0', 'example@domain.com', 'jquery@2.2', 'es5.shim@4.1', 'lodash@3.10', 'react@0.14', 'fitvids@1.1', 'jquery.slick@1.6', 'hola@ejemplo.com', 'name@example.com', 'titti@ponderosa.it', 'stefania@ponderosa.it', 'Susan.Tilly@musicsales.co', '8@7.k', 'M@dv.vݖ', 'x@C0.h', 'info@elrowfamily.com', 'hr@elrowfamily.com', 'TABLES@STUDIO338.CO', 'dave.plugandplay@gmail.com', 'tashsultanateam@paradigmagency.com', 'paulb@freetradeagency.co', 'rzifarelli@paradigmagency.com', 'admin@lemontreemusic.com', 'Qk@8.fy', '3@7.A', 'T@G.ݤ', 'Wq@G.Cr', 'b2binterfacesupport@miki.co', 'WorldAdSense@us.world', 'react-intl@2.4', 'robert@broofa.com', 'example@email.com', 'mautrechy@escpeurope.eu', 'crudisch@escpeurope.eu', 'kwolenska@escpeurope.eu', 'tfernandez@escpeurope.eu', 'lherold@escpeurope.eu', 'cmarinelli@escpeurope.eu', 'particles.js@2.0', 'akaplan@escpeurope.eu', 'tschmitz@escpeurope.eu', 'aiakovleva@escpeurope.eu', 'rwilken@escpeurope.eu', 'jehlers@escpeurope.eu', 'patrick.wolf@edu.escpeurope', 'angelica.zorzettig@edu.escpeurope', 'hallo@mirkokraeft.com', '4@h.5', 'info-erasmus@escpeurope.eu', 'vcacean@escpeurope.eu', 'info.de@escpeurope.eu', 'efett@escpeurope.eu', 'clehmann@escpeurope.eu', 'amechelhoff@escpeurope.eu', 'bkapteina@escpeurope.eu', 'achristodulu@escpeurope.eu', 'cklauth@escpeurope.eu', 'kgrimm@escpeurope.eu', 'library-berlin@escpeurope.eu', 'fmorrone@escpeurope.eu', 'ttse@escpeurope.eu', 'shoyez@escpeurope.eu', 'info.es@escpeurope.eu', 'info.it@escpeurope.eu', 'info.pl@escpeurope.eu', 'mail@ejemplo.com', 'admin@ijf.org', 'president@ijf.org', 'treasurer@ijf.org', 'gs@ijf.org', 'habibsissoko1@yahoo.fr', 'president@eju.net', 'mlarranaga@yahoo.com', 'president@oceaniajudo.com', 'juanbarcos@teleline.es', 'snijdersjan@eju.net', 'bartajudo@volny.cz', 'artem.judo@mail.ru', 'lascau@ijf.org', 'lisa@ijf.org', 'meridjajudoecc@yahoo.fr', 'benone@ijf.org', 'ijf@ijf.org', 'ajjf@judo.or', 'LSynkova@smpbank.ru', 'r.siteny@gmail.com', 'president@judo.az', 'feedback@wework.com', 'privacy@wework.com', 'DPO.Singapore@wework.com', 'joinus@wework.com', 'press@wework.com', 'visites.hdv@paris.fr', 'reception@1lombardstreet.com', 'office@thedonrestaurant.co', 'coqdargent@danddlondon.com', 'london.bookings@stonegatepubs.com', 'bun176133@mabretailemail.net', 'city@vinoteca.co', 'bookings@thedonrestaurant.co', 'tappithen@davy.co', 'manager@silkandgrain.co', 'enquiries@mrestaurants.co', 'threadneedlestreet@brasserieblanc.com', 'reservations@mintleaflounge.com', 'reservations@coyarestaurant.com', 'info@theindia.org', 'info@brigadierslondon.com', 'vipdesk@ytlhotels.co', 'info@mpwbank.com', 'woolgateexchange@davy.co', 'info@cabotte.co', 'oldewineshades@elvino.co', 'city@gauchorestaurants.com', 'masonsavenue@elvino.co', 'mansionhouse@thaisq.com', 'info@theanthologistbar.co', 'adams.court@ballsbrothers.co', 'info@lucsbrasserie.com', 'info@thefollybar.co', 'taberna@etruscarestaurants.com', 'bowlane@planetofthegrapes.co', 'reservations@citysociallondon.com', 'thegallery@ballsbrothers.co', 'reservations@templeandsons.co', 'info@chamberlainsoflondon.com', 'latasca.leadenhall@latasca.co', 'reservations@breadstreetkitchen.com', 'byron@byronhamburgers.com', 'madisoninfo@danddlondon.com', 'restaurants@skygarden.london', 'manager@thefactoryhouse.co', 'plantationplace@davy.co', 'enquires@boltonsrestaurant.co', 'info@foxfinewines.co', 'onenewchange@zizzi.co', 'informacion@congreso.es', 'info@chukaramenbar.com', 'askuabarra@gmail.com', 'hotelurban@derbyhotels.es', 'john.smith@gmail.com', 'media@impacthub.net', 'partnerships@impacthub.net', 'support@sports.fr', 'CustomerService@SuperShuttle.com', 'never@supershuttle.com', 'gabinetedeprensa@acciona.es', 'redessociales@acciona.com', 'inversores@acciona.es']


#Initiate stuff
driver = webdriver.Chrome('C:/Users/sai.vikranth/Documents/autobot/Google-Search-Result-Automation/Archive/chromedriver.exe') # UPDATE THIS PATH FOR YOUR LOCAL SYSTEM
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


# Literally does everything else
def everythingelse():
    global workbookName, emails, city, keywordPairs, language, perPage, driver, domains, numSuccessful, wordsFile, numResults, links
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

    # ACCUMULATE LINKS FOR EACH 
    for word in keywordPairs:
        searchquery = str(city + "+" + word[0])
        logging.info(str(datetime.datetime.now()) + ': Started searching for ' + searchquery)
        isActive = True
        start = 0
        currlinks = []

        while isActive:
            url = 'https://www.google.com/search?nl=' + language + '&q=' + searchquery + '&start=' + str(start) + '&num=' + str(perPage)
            try:
                driver.get(url)
                driver.find_element_by_class_name("g")
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")
                divs = soup.findAll("div", attrs={"class": "g"})
                for div in divs:
                    a = div.find("a")
                    link = a["href"]
                    domain = tldextract.extract(link)[1]
                    numResults += 1

                    if (domain not in domains and domain not in badDomains and link not in links):
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

            start += perPage
            time.sleep(random.randint(10, 15))
        
        logging.info(str(datetime.datetime.now()) + ': Completed searching for ' + searchquery)
        logging.info(str(datetime.datetime.now()) + ': Started email scraping for ' + searchquery)

        print(len(currlinks))
        print(numResults)

        # START SCRAPING FOR EMAILS
        for url in currlinks:
            em = ExtractEmails(url=url, depth=20, print_log=True, ssl_verify=True, user_agent='random')
            deseemails = em.emails
            if (len(deseemails) > 0):
                numSuccessful += 1
                for email in deseemails:
                    if email not in emails:
                        print(email)
                        emails.append(email)
                        exceltriples.append((url, email))
                        wsh.write(row, 0, email)
                        wsh.write(row, 1, url)
                        row += 1
    
    driver.close()
    book.close()
    logging.info(str(datetime.datetime.now()) + ': Completed a search, here are the stats: \n' + 'Number of entries: ' + str(len(exceltriples)) + '\n' + 'Number of results searched: ' + str(len(domains)) + "\nNumber of 'good' domains:" + str(len(domains)) + '\nNumber of domains with emails: ' + str(numSuccessful) + '\n' + 'Time Elapsed = ' + str((time.time() - start_time)))
    messagebox.showinfo('SUCCESS', 'Search completed :D')


# Handles the button clicks
def buttonHandler(text, thiscity, filename):
    global city, keywordPairs, cities, workbookName, wordsfile
    reset()
    workbookName = filename
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