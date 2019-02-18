from urllib import request
from urllib.request import Request, urlopen
import re
import tldextract

from googlesearch import search 

webURL = 'https://www.timeout.com/'

extraction = tldextract.extract(webURL)
domain = extraction[1]
print(domain)