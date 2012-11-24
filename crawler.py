#    Author      : Abhay Jain
#    Language    : Python3.2
#    File        : crawler.py
#    Description : This is a simple web crawler which begins crawling with given seed URL
#
##-----------------------------------------------------------------------------------------------------

from bs4 import BeautifulSoup

import urllib.request
import re

def is_url_valid(url):
    '''
        (str) -> boolean

        This method takes a url as input and returns true if this url is valid.
        URL is assumed valid only if it begins with https:// or http:// or www. in lower case string'''
    
    pattern1 = '^http://'
    pattern2 = '^https://'
    pattern3 = '^www\.'
    url = url.lower()
    
    if re.search(pattern1, url) or re.search(pattern2, url) or re.search(pattern3, url):
        return True
    return False
    
def merge(list_a, list_b):
    '''
        (list, list) -> list

        This method returns union of list_a and list_b '''
    
    for link in list_b:
        if link not in list_a:
            list_a.append(link)

def get_links_on_page(url):
    '''
        (str) -> list

        This method takes as input a url and returns list of
        hyperlinks on that url page. '''
    
    links = []
    socket = urllib.request.urlopen(url)
    html_page = socket.read()

    # List of hyperlinks is created by assuming only
    # <a href='link'> HTML tags in page contains crawlable links
    page_str = BeautifulSoup(html_page)
    list_of_tags = page_str.findAll("a")
            
    for tag in list_of_tags:
        links.append(tag.get('href'))
        
    return links

def crawler(seed_url, max_links):
    '''
        (str, int) -> list
        
         This is main function which takes as input a seed url to begin crawl
         and maximum number of links after which crawling stops. It returns list
         of crawled urls.'''
         
    remaining_links = [seed_url]
    finished_links = []

    # Stop crawling when there are no more links to be crawled
    # or when limit of crawling links has been reached
    while remaining_links and len(finished_links) < max_links :
        url = remaining_links.pop()

        # Crawl url only when it has not been crawled already
        # and this links is crawlable
        if url not in finished_links and is_url_valid(url):
            try:
                links = get_links_on_page(url)
                merge(remaining_links, links)
                finished_links.append(url)
            except:
                # Dont process URL if there were some HTTP errors
                pass
            
    return finished_links


if __name__ == '__main__':

    # URL with no hyperlinks
    seed_url = "http://www.this-page-intentionally-left-blank.org/"
    max_links = 5
    crawled_links = crawler(seed_url, max_links)
    print (crawled_links)

    # Invalid URL
    seed_url = "abcd"
    max_links = 10
    crawled_links = crawler(seed_url, max_links)
    print (crawled_links)

    # Google homepage
    seed_url = "http://www.google.co.in/"
    max_links = 6
    crawled_links = crawler(seed_url, max_links)
    print (crawled_links)

    # Python homepage
    seed_url = "http://python.org/"
    max_links = 8
    crawled_links = crawler(seed_url, max_links)
    print (crawled_links)

    # Yahoo homepage
    seed_url = "http://in.yahoo.com/"
    max_links = 10
    crawled_links = crawler(seed_url, max_links)
    print (crawled_links)
