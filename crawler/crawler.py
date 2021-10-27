from bs4 import BeautifulSoup
import requests
import urllib.robotparser
import ssl
from time import sleep

ssl._create_default_https_context = ssl._create_unverified_context

# seed = "https://vinhofacil.com.br"

# rp = urllib.robotparser.RobotFileParser()
# rp.set_url(f"{seed}/robots.txt")
# rp.read()

# print(rp.can_fetch("*", "https://vinhofacil.com.br/vinhos"))

def process_url(url, root):
    if (url.startswith('/')):
        return f"{root}{url}"

    return url

def check_url(url, root):
    # Don't access Disallowed routes by robots.txt
    # if (rp.can_fetch("*", url)):
    
    if (url.startswith('/')):
        return True

    if (url.startswith(root)):
        return True
    
    if (url == root):
        return True
    
    return False


def get_page_urls(start):
    urls = set()
    urls.add(start)

    html = requests.get(start)
    soup = BeautifulSoup(html.text, "html.parser")

    all_anchors = soup.find_all('a', href=True)

    for anchor in all_anchors:
        url = anchor["href"]

        # Check if url is usable
        processed = process_url(url, start)

        if (check_url(processed, start)):
            urls.add(processed)
    
    return urls

def bsf_crawl(seed):
    visited = set()
    edge = [seed]
    count = 0

    while (len(edge) > 0 and len(visited) < 100):
        current = edge.pop(0)

        if (not current in visited):
            visited.add(current)
            new_urls = get_page_urls(current)
            edge.extend(new_urls)
            sleep(0.01)

            count += 1

            print(f"Entered {current}")
    
    print(f"Visited {count} pages")



def main():
    bsf_crawl("https://vinhofacil.com.br")

if __name__ == "__main__":
    main()