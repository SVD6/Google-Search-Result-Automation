from googlesearch import search 
import xlsxwriter
import tldextract

filename = 'test123'

book = xlsxwriter.Workbook(filename + '.xlsx')
wsh = book.add_worksheet()

bold = book.add_format({'bold': 1})
wsh.set_column(0, 2, 30)  
wsh.write('A1', 'Website Title', bold)
wsh.write('B1', 'Website Link', bold)
wsh.write('C1', 'Contact Email', bold)


book.close()



urls = []
links = []
stop = 0

searchquery = "madrid tours"
numresults = 20

for webURL in search(searchquery, tld='ca', safe='off', start=0, pause=2):

    if (stop == (numresults + 1)):
        break 

    extraction = tldextract.extract(webURL)
    domain = extraction.domain()

    if (domain not in urls and domain != 'airbnb' and domain != 'facebook' and domain != 'tripadvisor' and domain != 'kayak' 
    and domain != 'expedia' and domain != 'viator' and domain != 'getyourguide' and domain != 'youtube' and domain != 'amazon'):
        print(domain)
        urls.append(domain)
        links.append(webURL)
    
    stop += 1