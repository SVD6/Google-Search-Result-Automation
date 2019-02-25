import requests
import tldextract
import selenium

from googlesearch import search 
from bs4 import BeautifulSoup
from selenium import webdriver
from re import match, findall

NoSuchElementException = selenium.common.exceptions.NoSuchElementException

def _get_number_of_results(results_div):
    """Return the total number of results of the google search.
    Note that the returned value will be the same for all the GoogleResult
    objects from a specific query."""
    try:
        results_div_text = results_div.get_text()
        if results_div_text:
            regex = r"((?:\d+[,\.])*\d+)"
            m = findall(regex, results_div_text)

            # Clean up the number.
            num = m[0].replace(",", "").replace(".", "")

            results = int(num)
            return results
    except Exception as e:
        print("Can't find results" + str(e))
        return 0

searchquery = 'Madrid Tours'

language = 'en'

start = '20'

num = '10'

url = 'https://www.google.com/search?nl=' + language + '&q=' + searchquery + '&start=' + start + '&num=' + num
disurl = 'https://www.google.com/search?nl=en&q=Madrid+Tours&num=30&start=10'

isresult = True

driver = webdriver.Chrome('C:/Users/sai.vikranth/Documents/autobot/Google-Search-Result-Automation/Archive/chromedriver.exe')
driver.get(disurl)
html = driver.page_source
try:
    driver.find_element_by_class_name("g")
except NoSuchElementException:
    print('No searchresults here')
testing = html.find("did not match any documents.")

print(testing)


soup = BeautifulSoup(html, "html.parser")
try:
    divs = soup.findAll("div", attrs={"class": "g"})
except NoSuchElementException:
    print ('No search results here')
for div in divs:
    a = div.find("a")
    link = a["href"]
    domain = tldextract.extract(link)[1]
    print(domain)
print(len(divs))


# for each in divs:
#     try:
#         a = each.find("a")
#         link = a["href"]
#     except Exception:
#         print('Error')

#     if link.startswith("/url?") or link.startswith("/search?"):
#         print(link)

#     else:
#         print('Error')

driver.close()
driver.quit()
