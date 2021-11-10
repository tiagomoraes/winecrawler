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
('adegamais', 'https://adegamais.com.br'),
('vivavinho', 'https://www.vivavinho.com.br'),
('wine', 'https://www.wine.com.br')]

seeds=[('viavini', 'https://www.viavini.com.br')]

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
            sleep(0.1)

            print(f'Entered {current}')
    
    print(f'Visited {count} pages')

# ========== HEURISTIC ==========
'''
The baisc heuristic used here, prioritizes the wanted
terms and discards non wanted terms on the text or href
'''

WANTED_PATHS = ['/p/', '/produto', '/product', '/prod', 
'/item', '/vinho']

WANTED_TERMS = ['tinto', 'branco', 'espumante', 'rose', 
'rosado', 'cabernet', 'malbec', 'shiraz', 'primitivo', 
'merlot', 'garnacha', 'pinot', 'carmenere', 'brut', 
'mosacatel', 'tempranillo', 'reserva','chardonnay', 
'riesling', 'seco', 'ver', 'mais']

NOT_WANTED_PATHS = ['/kits?', '/carrinho', '/cart', 
'/sacola', '/add/']

NOT_WANTED_TERMS = ['kits?', 'saca', 'ta(ç|c)a', 
'contato', 'sobre', 'carrinho', 'termo', 'sacola',
'pol(í|i)tica', 'acess(ó|o)rios', 'blog', 'central']

def classify_anchor(anchor):
    weight = 0

    for term in WANTED_PATHS:
        if anchor['href'] and re.match(f'.*{term}.*', anchor['href'].lower()):
            weight = weight + 20
    
    for term in WANTED_TERMS:
        if anchor.text and re.match(f'.*{term}.*', anchor.text.lower()):
            weight = weight + 10

    for term in NOT_WANTED_PATHS:
        if anchor['href'] and re.match(f'.*{term}.*', anchor['href'].lower()):
            weight = weight - 20

    for term in NOT_WANTED_TERMS:
        if anchor.text and re.match(f'.*{term}.*', anchor.text.lower()):
            weight = weight - 10
        
    return weight


def save_and_get_page_urls_with_heuristic(start, seed, robots, count):
    urls = set()

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
        classification = classify_anchor(anchor)
        url = anchor['href']
        processed = process_url(url, seed[1])

        # Check if url is usable
        if (check_url(processed, seed[1], robots)):
            urls.add((processed, classification))

    return urls

# take second element for sort
def takeSecond(elem):
    return elem[1]

def heuristic_crawl(seed):
    robots = Robots.fetch(f'{seed[1]}/robots.txt')

    visited = set()
    edge = [(seed[1], 0)]
    count = 0

    while (len(edge) > 0 and len(visited) < 1000):
        edge.sort(key=takeSecond, reverse=True)
        current = edge.pop(0)

        if (not current[0] in visited):
            visited.add(current[0])
            count += 1

            new_urls = save_and_get_page_urls_with_heuristic(current[0], seed, robots, count)
            edge.extend(new_urls)
            sleep(0.1)

            print(f'Entered {current}')
    
    print(f'Visited {count} pages')


def main():
    pool = Pool(10)
    pool.map(heuristic_crawl, seeds)
    pool.close()
    pool.join()

if __name__ == '__main__':
    main()