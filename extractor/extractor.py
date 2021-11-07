from bs4 import BeautifulSoup
import requests
import re
import ssl
from time import sleep
from tabulate import tabulate

ssl._create_default_https_context = ssl._create_unverified_context

def wine_extract(soup):
    name = None
    name_marker = soup.find('h1', attrs={'class': 'PageHeader-title'})
    if (name_marker):
        name = name_marker.text

    type = None
    type_marker = soup.find(text=re.compile('.*Tipo.*', re.DOTALL))
    if (type_marker):
        type = type_marker.parent.find_next('dd').text

    grape = None
    grape_marker = soup.find(text=re.compile('.*Uva.*', re.DOTALL))
    if (grape_marker):
        grape = grape_marker.parent.find_next('dd').text
    
    country = None
    country_marker = soup.find(text=re.compile('.*País.*', re.DOTALL))
    if (country_marker):
        country = country_marker.parent.find_next('dd').text
    
    classification = None
    classification_marker = soup.find(text=re.compile('.*Classificação.*', re.DOTALL))
    if (classification_marker):
        classification = classification_marker.parent.find_next('dd').text

    alcohol_content = None
    alcohol_content_marker = soup.find(text=re.compile('.*Teor.*', re.DOTALL))
    if (alcohol_content_marker):
        alcohol_content = alcohol_content_marker.parent.find_next('dd').text
    
    year = None
    year_marker = soup.find(text=re.compile('.*Safra.*', re.DOTALL))
    if (year_marker):
        year = year_marker.parent.find_next('dd').text

    return({
        'name': name,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })

def evino_extract(soup):
    name = None
    name_marker = soup.find('h2', itemprop='name')
    if (name_marker):
        name = name_marker.text

    type = None
    type_marker = soup.find('h4', text=re.compile('.*Tipo.*', re.DOTALL))
    if (type_marker):
        type = type_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text

    grape = None
    grape_marker = soup.find('h4', text=re.compile('.*Uva.*', re.DOTALL))
    if (grape_marker):
        grape = grape_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text

    country = None
    country_marker = soup.find('h4', text=re.compile('.*País.*', re.DOTALL))
    if (country_marker):
        country = country_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text
    
    classification = None
    classification_marker = soup.find(lambda tag:tag.name=='h4' and 'Classificação' in tag.text)
    if (classification_marker):
        classification = classification_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text

    alcohol_content = None
    alcohol_content_marker = soup.find('h4', text=re.compile('.*Teor.*', re.DOTALL))
    if (alcohol_content_marker):
        alcohol_content = alcohol_content_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text
    
    year = None
    year_marker = soup.find('h4', text=re.compile('.*Safra.*', re.DOTALL))
    if (year_marker):
        year = year_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text
    
    return({
        'name': name,
        'type': type,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })

def vinhofacil_extract(soup):
    name = None
    name_marker = soup.find('h1', attrs={'class': 'h1 mb-1'})
    if (name_marker):
        name = name_marker.text

    type = None
    type_marker = soup.find('strong', text=re.compile('.*Tipo.*', re.DOTALL))
    if (type_marker):
        type = type_marker.parent.parent.find(text=True, recursive=False).strip(' ')

    grape = None
    grape_marker = soup.find('strong', text=re.compile('.*Uva.*', re.DOTALL))
    if (grape_marker):
        grape = grape_marker.parent.parent.find(text=True, recursive=False).strip(' ')
    
    country = None
    country_marker = soup.find('strong', text=re.compile('.*País.*', re.DOTALL))
    if (country_marker):
        country = country_marker.parent.parent.find(text=True, recursive=False).strip(' ')
    
    classification = None
    classification_marker = soup.find('strong', text=re.compile('.*Classificação.*', re.DOTALL))
    if (classification_marker):
        classification = classification_marker.parent.parent.find(text=True, recursive=False).strip(' ')

    alcohol_content = None
    alcohol_content_marker = soup.find('strong', text=re.compile('.*Teor.*', re.DOTALL))
    if (alcohol_content_marker):
        alcohol_content = alcohol_content_marker.parent.parent.find(text=True, recursive=False).strip(' ')
    
    year = None
    year_marker = soup.find('strong', text=re.compile('.*Safra.*', re.DOTALL))
    if (year_marker):
        year = year_marker.parent.parent.find(text=True, recursive=False).strip(' ')

    return({
        'name': name,
        'type': type,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })

def grandcru_extract(soup):
    name = None
    name_marker = soup.find('h1', attrs={'class': 'product-title'})
    if (name_marker):
        name = name_marker.find('span').text.replace('\n', '').strip(' ')

    type = None
    type_marker = soup.find('span', attrs={'class': 'tipo-vinho'})
    if (type_marker):
        type = type_marker.find('small').text

    grape = None
    grape_marker = soup.find('span', attrs={'class': 'uva'})
    if (grape_marker):
        grape = grape_marker.find('small').text
    
    country = None
    country_marker = soup.find('label', text=re.compile('.*País.*', re.DOTALL))
    if (country_marker):
        country = country_marker.parent.find('span').text
    
    classification = None
    classification_marker = soup.find('label', text=re.compile('.*Classificação.*', re.DOTALL))
    if (classification_marker):
        classification = classification_marker.parent.find('span').text

    alcohol_content = None
    alcohol_content_marker = soup.find('span', attrs={'class': 'teor'})
    if (alcohol_content_marker):
        alcohol_content = alcohol_content_marker.find('small').text
    
    year = None
    year_marker = soup.find('span', attrs={'class': 'safra'})
    if (year_marker):
        year = year_marker.find('small').text

    return({
        'name': name,
        'type': type,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })

def mistral_extract(soup):
    name = None
    name_marker = soup.find('h1', attrs={'class': 'name-wine-product-new'})
    if (name_marker):
        name = name_marker.text

    type = None
    type_marker = soup.find('p', text=re.compile('.*Tipo.*', re.DOTALL))
    if (type_marker):
        type = type_marker.findNext('p').text

    grape = None
    grape_marker = soup.find('p', text=re.compile('.*Uva.*', re.DOTALL))
    if (grape_marker):
        grape = grape_marker.findNext('p').text

    country = None
    country_marker = soup.find('p', text=re.compile('.*País.*', re.DOTALL))
    if (country_marker):
        country = country_marker.findNext('p').text
    
    classification = None
    classification_marker = soup.find('p', text=re.compile('.*Classificação.*', re.DOTALL))
    if (classification_marker):
        classification = classification_marker.findNext('p').text

    alcohol_content = None
    alcohol_content_marker = soup.find('p', text=re.compile('.*Teor.*', re.DOTALL))
    if (alcohol_content_marker):
        alcohol_content = alcohol_content_marker.findNext('p').text
    
    year = None
    year_marker = soup.find('p', text=re.compile('.*Safra.*', re.DOTALL))
    if (year_marker):
        year = year_marker.findNext('p').text

    return({
        'name': name,
        'type': type,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })
    
def extract(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    print(mistral_extract(soup))

def main():
    extract('https://www.mistral.com.br/p/vinho/lapostolle-grand-selection-cabernet-sauvignon-2017-lapostolle')

if __name__ == '__main__':
    main()