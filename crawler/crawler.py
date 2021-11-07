from bs4 import BeautifulSoup
import requests
import re
# import urllib.robotparser
import ssl
from time import sleep

# TODO
# 1. Respect robots.txt
# 2. Verify usable pages

ssl._create_default_https_context = ssl._create_unverified_context

# seed = 'https://vinhofacil.com.br'

# rp = urllib.robotparser.RobotFileParser()
# rp.set_url(f'{seed}/robots.txt')
# rp.read()

def process_url(url, root):
    if (url.startswith('/')):
        return f'{root}{url}'

    return url

def check_url(url, root):
    # Don't access Disallowed routes by robots.txt
    # if (rp.can_fetch('*', url)):

    # Remove long urls (avoid qp loops)
    if (len(url) > 160):
        return False
    
    if (url.startswith('/') or
        url.startswith(root) or 
        url == root):
        # Means url is usable
        return True

    return False


def get_page_urls(start, seed):
    urls = set()
    urls.add(start)

    hr = requests.head(start)

    if (not 'content-type' in hr.headers):
        return urls

    if (not hr.headers['content-type'].startswith('text/html')):
        return urls

    html = requests.get(start)
    soup = BeautifulSoup(html.text, 'html.parser')

    all_anchors = soup.find_all('a', href=True)

    for anchor in all_anchors:
        url = anchor['href']

        # Check if url is usable
        processed = process_url(url, seed)

        if (check_url(processed, seed)):
            urls.add(processed)
    
    return urls

def bfs_crawl(seed):
    visited = set()
    edge = [seed]
    count = 0

    while (len(edge) > 0 and len(visited) < 1000):
        current = edge.pop(0)

        if (not current in visited):
            visited.add(current)
            new_urls = get_page_urls(current, seed)
            edge.extend(new_urls)
            sleep(0.01)

            count += 1

            print(f'Entered {current}')
    
    print(f'Visited {count} pages')

# ========== HEURISTIC ==========
'''
The baisc heuristic used here, finds all the anchors
that have the word 'vinho' on the anchor text or href
'''
def get_page_urls_with_heuristic(start, seed):
    urls = set()

    hr = requests.head(start)

    if (not 'content-type' in hr.headers):
        return urls

    if (not hr.headers['content-type'].startswith('text/html')):
        return urls

    html = requests.get(start)
    soup = BeautifulSoup(html.text, 'html.parser')

    all_anchors = soup.find_all('a', href=True)

    for anchor in all_anchors:
        # Only add anchors that have the word wine on it
        if (anchor.find(string=re.compile('.*vinho.*', re.DOTALL)) or
            anchor.find(string=re.compile('.*Vinho.*', re.DOTALL)) or
            anchor.find(href=re.compile('.*vinho.*', re.DOTALL)) or
            anchor.find(alt=re.compile('.*vinho.*', re.DOTALL)) or
            anchor.find(string=re.compile('.*kit.*', re.DOTALL)) or
            anchor.find(string=re.compile('.*tinto.*', re.DOTALL)) or
            anchor.find(string=re.compile('.*branco.*', re.DOTALL)) or
            anchor.find(string=re.compile('.*espumante.*', re.DOTALL)) or
            anchor.find(string=re.compile('.*product.*', re.DOTALL)) or
            anchor.find(string=re.compile('.*rose.*', re.DOTALL))
        ):
            url = anchor['href']

            # Check if url is usable
            processed = process_url(url, seed)

            if (check_url(processed, seed)):
                urls.add(processed)
    
    return urls


def heuristic_crawl(seed):
    visited = set()
    edge = [seed]
    count = 0

    while (len(edge) > 0 and len(visited) < 1000):
        current = edge.pop(0)

        if (not current in visited):
            visited.add(current)
            new_urls = get_page_urls_with_heuristic(current, seed)
            edge.extend(new_urls)
            sleep(0.01)

            count += 1
            
            print(f'Entered {current}')
    
    print(f'Visited {count} pages')


def main():
    bfs_crawl('https://www.grandcru.com.br')

if __name__ == '__main__':
    main()