import requests

from googlesearch import search 
from fake_useragent import UserAgent
from lxml import html
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

ua = UserAgent()
agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
            'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
            'safari': ua.safari, 'random': ua.random}
url = 'https://www.airbnb.ca/experiences/468150?location=Madrid%2C%20Spain&source=p2&currentTab=experience_tab&searchId=4b2a4b5f-55b7-4c1e-8297-bf67749af7a3&federatedSearchId=7b9ed34c-86b7-4b3c-aa68-219a08044a33&sectionId=53a6dbad-a31b-49fa-9aa1-3b336a300da4'

# driver = webdriver.Chrome(ChromeDriverManager().install())
# driver.get(url)

headers = {'User-Agent': agents['chrome']}
r = requests.get(url, headers = headers, verify = True)

soup = BeautifulSoup(r.text)
t = soup.title
print(t.contents[0])

