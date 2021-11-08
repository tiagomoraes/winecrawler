from bs4 import BeautifulSoup
import requests
import re
from reppy.robots import Robots
from multiprocessing import Pool
import os
import ssl
from time import sleep

ssl._create_default_https_context = ssl._create_unverified_context

seeds=[('divinho', 'https://www.divinho.com.br'), 
('divvino', 'https://www.divvino.com.br'), 
('evino', 'https://www.evino.com.br'),
('grandcru', 'https://www.grandcru.com.br'),
('mistral', 'https://www.mistral.com.br'),
('superadega', 'https://www.superadega.com.br'),
('viavini', 'https://www.viavini.com.br'),
('vinhofacil', 'https://www.vinhofacil.com.br'),
('vivavinho', 'https://www.vivavinho.com.br'),
('wine', 'https://www.wine.com.br')]

def process_url(url, root):
    if (url.startswith('/')):
        return f'{root}{url}'

    return url

def check_url(url, root, robots):
    # Don't access Disallowed routes by robots.txt
    if (not robots.allowed(url, '*')):
        return False
    
    # Remove long urls (avoid qp loops)
    if (len(url) > 160):
        return False
    
    if (url.startswith('/') or
        url.startswith(root) or 
        url == root):
        # Means url is usable
        return True

    return False


def save_and_get_page_urls(start, seed, robots, count):
    urls = set()
    urls.add(start)

    # Check headers if response is html text
    try:
        hr = requests.head(start)

        if (not 'content-type' in hr.headers):
            return urls

        if (not hr.headers['content-type'].startswith('text/html')):
            return urls
    except:
        return urls

    html = requests.get(start)

    file = f'./bfs_pages/{seed[0]}/{count}.html'
    os.makedirs(os.path.dirname(file), exist_ok=True)

    f = open(file, 'w')
    f.write(html.text)
    f.close()

    soup = BeautifulSoup(html.text, 'html.parser')

    all_anchors = soup.find_all('a', href=True)

    for anchor in all_anchors:
        url = anchor['href']

        # Check if url is usable
        processed = process_url(url, seed[1])

        if (check_url(processed, seed[1], robots)):
            urls.add(processed)
    
    return urls

def bfs_crawl(seed):
    robots = Robots.fetch(f'{seed[1]}/robots.txt')

    visited = set()
    edge = [seed[1]]
    count = 0

    while (len(edge) > 0 and len(visited) < 1000):
        current = edge.pop(0)

        if (not current in visited):
            visited.add(current)
            count += 1

            new_urls = save_and_get_page_urls(current, seed, robots, count)
            edge.extend(new_urls)
            sleep(0.01)

            print(f'Entered {current}')
    
    print(f'Visited {count} pages')

# ========== HEURISTIC ==========
'''
The baisc heuristic used here, finds all the anchors
that have the word 'vinho' on the anchor text or href
'''
def save_and_get_page_urls_with_heuristic(start, seed, robots, count):
    urls = set()
    urls.add(start)

    # Check headers if response is html text
    try:
        hr = requests.head(start)

        if (not 'content-type' in hr.headers):
            return urls

        if (not hr.headers['content-type'].startswith('text/html')):
            return urls
    except:
        return urls

    html = requests.get(start)

    file = f'./heuristic_pages/{seed[0]}/{count}.html'
    os.makedirs(os.path.dirname(file), exist_ok=True)

    f = open(file, 'w')
    f.write(html.text)
    f.close()

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
            processed = process_url(url, seed[1])

            if (check_url(processed, seed[1], robots)):
                urls.add(processed)
    
    return urls


def heuristic_crawl(seed, robots):
    visited = set()
    edge = [seed[1]]
    count = 0

    while (len(edge) > 0 and len(visited) < 1000):
        current = edge.pop(0)

        if (not current in visited):
            visited.add(current)
            count += 1

            new_urls = save_and_get_page_urls_with_heuristic(current, seed, robots, count)
            edge.extend(new_urls)
            sleep(0.01)

            print(f'Entered {current}')
    
    print(f'Visited {count} pages')


def main():
    pool = Pool(10)
    pool.map(bfs_crawl, seeds)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()