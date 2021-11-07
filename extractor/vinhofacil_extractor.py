from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


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

    return ({
        'name': name,
        'type': type,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })


def main():
    html = requests.get('')
    soup = BeautifulSoup(html.text, 'html.parser')

    print(vinhofacil_extract(soup))


if __name__ == '__main__':
    main()
