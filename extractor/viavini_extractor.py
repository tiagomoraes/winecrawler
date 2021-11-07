from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def viavini_extract(big_soup):
    soup = big_soup.find('div', attrs={'class': 'datasheet-box'})

    name = None
    name_marker = big_soup.find('span', itemprop="name")
    if name_marker:
        name = name_marker.text

    wine_type = None
    wine_type_marker = soup.find('h6', text=re.compile('.*Tipo.*', re.DOTALL))
    if wine_type_marker:
        wine_type = wine_type_marker.findNext('p').text
    
    grape = None
    grape_marker = soup.find('h6', text=re.compile('.*Uva.*', re.DOTALL))
    if grape_marker:
        grape = grape_marker.findNext('p').text

    country = None
    country_marker = soup.find('div', attrs={'class': 'datasheet-item-text'})
    if country_marker:
        country_new_marker = country_marker.find('h6', attrs={'class': 'attribute-name'})
        if country_new_marker:
            country = country_new_marker.text

    classification = None
    classification_marker = soup.find('h6', text=re.compile('.*Classificação.*', re.DOTALL))
    if classification_marker:
        classification = classification_marker.findNext('p').text

    alcohol_content = None
    alcohol_content_marker = soup.find('h6', text=re.compile('.*Teor.*', re.DOTALL))
    if alcohol_content_marker:
        alcohol_content = alcohol_content_marker.findNext('p').text.replace('°', '%')

    year = None
    year = soup.find('h6', text=re.compile('.*Safra.*', re.DOTALL))
    if year:
        year = year.findNext('p').text

    return ({
        'name': name,
        'wine_type': wine_type,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })


def main():
    html = requests.get('https://www.viavini.com.br/vinho-primitivo-di-manduria-80-vecchie-vigne-ottantanni-tinto-italiano.html')
    soup = BeautifulSoup(html.text, 'html.parser')

    print(viavini_extract(soup))


if __name__ == '__main__':
    main()
