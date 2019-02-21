import os
import random
import sys
import time
import math
import requests

from fake_useragent import UserAgent
from urllib.parse import quote_plus, urlparse, parse_qs
from bs4 import BeautifulSoup

ua = UserAgent()
agents = {'ie': ua.ie, 'msie': ua.msie, 'opera': ua.opera,
              'chrome': ua.chrome, 'google': ua.google, 'firefox': ua.firefox,
              'safari': ua.safari, 'random': ua.random}

class TimeoutException(Exception): pass


# URL templates to make Google searches.
url_home = "https://www.google.%(tld)s/"
url_search = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
             "btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s"
url_next_page = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                "start=%(start)d&tbs=%(tbs)s&safe=%(safe)s&tbm=%(tpe)s"
url_search_num = "https://www.google.%(tld)s/search?hl=%(lang)s&q=%(query)s&" \
                 "num=%(num)d&btnG=Google+Search&tbs=%(tbs)s&safe=%(safe)s&" \
                 "tbm=%(tpe)s"
url_next_page_num = "https://www.google.%(tld)s/search?hl=%(lang)s&" \
                    "q=%(query)s&num=%(num)d&start=%(start)d&tbs=%(tbs)s&" \
                    "safe=%(safe)s&tbm=%(tpe)s"

def get_page(url, user_agent):
    if user_agent is None:
        user_agent = agents[random]

    try:
        headers = {
            'User-Agent': agents[user_agent]}
    except:
        headers = {
            'User-Agent': user_agent
        }

    try:
        r = requests.get(url, headers=headers, verify=True, timeout=5.0)
        print('googlesearch request')
        return r.text
    except Exception:
        print('Error sending request, googlesearch2.py')
        return 'bad'
        
    
# Method to filter results
def filter_result(link):
    try:
        # Valid results are absolute URLs not pointing to a Google domain
        # like images.google.com or googleusercontent.com
        o = urlparse(link, 'http')
        if o.netloc and 'google' not in o.netloc:
            return link

        # Decode hidden URLs.
        if link.startswith('/url?'):
            link = parse_qs(o.query)['q'][0]
            # Valid results are absolute URLs not pointing to a Google domain
            # like images.google.com or googleusercontent.com
            o = urlparse(link, 'http')
            if o.netloc and 'google' not in o.netloc:
                return link
    # Otherwise, or on error, return None.
    except Exception:
        pass
    return None

def search(query, tld, lang, tbs, safe, num, start, stop, domains, pause, only_standard, extra_params, tpe, user_agent):
    hashes = set()

    # Prepare domain list if it exists.
    if domains:
        domain_query = '+OR+'.join('site:' + domain for domain in domains)
    else:
        domain_query = ''

    # Prepare the search string.
    query = quote_plus(query + '+' + domain_query)

    # Check extra_params for overlapping
    for builtin_param in ('hl', 'q', 'btnG', 'tbs', 'safe', 'tbm'):
        if builtin_param in extra_params.keys():
            raise ValueError(
                'GET parameter "%s" is overlapping with \
                the built-in GET parameter',
                builtin_param
            )

    # Prepare the URL of the first request.
    if start:
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
    else:
        if num == 10:
            url = url_search % vars()
        else:
            url = url_search_num % vars()

    # Loop until we reach the maximum result, if any (otherwise, loop forever).
    while not stop or start < stop:

        try:  # Is it python<3?
            iter_extra_params = extra_params.iteritems()
        except AttributeError:  # Or python>3?
            iter_extra_params = extra_params.items()
        # Append extra GET_parameters to URL
        for k, v in iter_extra_params:
            url += url + ('&%s=%s' % (k, v))

        # Sleep between requests.
        time.sleep(pause)

        # Request the Google Search results page.
        html = get_page(url, user_agent)

        if (html == 'bad'):
            start += num
            if num == 10:
                url = url_next_page % vars()
            else:
                url = url_next_page_num % vars()
            print ('Bad 126')
            continue

        # Parse the response and process every anchored URL.
        soup = BeautifulSoup(html, 'html.parser')
        anchors = soup.find(id='search').findAll('a')

        for a in anchors:
            # Leave only the "standard" results if requested.
            # Otherwise grab all possible links.
            if only_standard and (not a.parent or a.parent.name.lower() != "h3"):
                print('Standard shit 141')
                continue

            # Get the URL from the anchor tag.
            try:
                link = a['href']
            except KeyError:
                print ('Exception 147')
                continue

            # Filter invalid links and links pointing to Google itself.
            link = filter_result(link)
            if not link:
                print ('Already there link 153')
                continue

            # Discard repeated results.
            h = hash(link)
            if h in hashes:
                print ('Not sure apparently in hashes 159')
                continue
            hashes.add(h)

            # Yield the result.
            yield link

        # End if there are no more results.
        if not soup.find(id='nav'):
            print ('No more results 168')
            break

        # Prepare the URL for the next request.
        start += num
        if num == 10:
            url = url_next_page % vars()
        else:
            url = url_next_page_num % vars()
