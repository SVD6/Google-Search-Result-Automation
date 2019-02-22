from google import standard_search
from extract_emails import ExtractEmails
import tldextract
import time
import random

results = 100
links = []
domains = []
goodemails = []
query = 'Madrid tours'
numgooglefound = 0
firstpage = 1
pagestosearch = int(((results - numgooglefound) / 10) + 1)
print(pagestosearch)

while numgooglefound < results:
    for link in standard_search.search(query=query, pages=pagestosearch, first_page=firstpage):
        if (numgooglefound == results):
            pass
        else:
            links.append(link.link)
            domain = tldextract.extract(link.link)[1]

            if (domain not in domains):
                numgooglefound += 1
                domains.append(domain)
                print(domain)
                try:
                    em = ExtractEmails(link.link, depth=30, print_log=True, ssl_verify=True, user_agent='random')
                except Exception:
                    print ('Problem')
                emails = em.emails
                if (len(emails) > 0):
                    for email in emails:
                        goodemails.append(email)

    firstpage += pagestosearch
    pagestosearch = int(((results - numgooglefound) / 10) + 3)
    time.sleep(random.randint(10, 20))
    
print(len(links))
print(firstpage)
print(numgooglefound)
print(goodemails)