from urllib import request
from urllib.request import Request, urlopen
import re

link = 'https://www.timeout.com/'

req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read().decode('utf-8')

# print(webpage)
emails = re.findall(r'[\w\.-]+@[\w\.-]+', webpage) 

for email in emails:
    print(email)

# reg_ex = re.compile(r'[-a-z0-9._]+@([-a-z0-9]+)(\.[-a-z0-9]+)+', re.IGNORECASE
