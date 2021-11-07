from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def global_extract(soup):
    name = None
    wine_type = None
    grape = None
    country = None
    classification = None
    alcohol_content = None
    year = None
    
    return({
        'name': name,
        'wine_type': wine_type,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })

def main():
    html = requests.get('')
    soup = BeautifulSoup(html.text, 'html.parser')

    print(global_extract(soup))


if __name__ == '__main__':
    main()