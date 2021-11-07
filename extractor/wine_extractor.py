from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def wine_extract(soup):
    name = None
    name_marker = soup.find('h1', attrs={'class': 'PageHeader-title'})
    if name_marker:
        name = name_marker.text

    wine_type = None
    type_marker = soup.find(text=re.compile('.*Tipo.*', re.DOTALL))
    if type_marker:
        wine_type = type_marker.parent.find_next('dd').text

    grape = None
    grape_marker = soup.find(text=re.compile('.*Uva.*', re.DOTALL))
    if grape_marker:
        grape = grape_marker.parent.find_next('dd').text

    country = None
    country_marker = soup.find(text=re.compile('.*País.*', re.DOTALL))
    if country_marker:
        country = country_marker.parent.find_next('dd').text

    classification = None
    classification_marker = soup.find(text=re.compile('.*Classificação.*', re.DOTALL))
    if classification_marker:
        classification = classification_marker.parent.find_next('dd').text

    alcohol_content = None
    alcohol_content_marker = soup.find(text=re.compile('.*Teor.*', re.DOTALL))
    if alcohol_content_marker:
        alcohol_content = alcohol_content_marker.parent.find_next('dd').text

    year = None
    year_marker = soup.find(text=re.compile('.*Safra.*', re.DOTALL))
    if year_marker:
        year = year_marker.parent.find_next('dd').text

    return ({
        'name': name,
        'type': wine_type,
        'grape': grape,
        'country': country,
        'classification': classification,
        'alcohol_content': alcohol_content,
        'year': year,
    })


def main():
    html = requests.get('')
    soup = BeautifulSoup(html.text, 'html.parser')

    print(wine_extract(soup))


if __name__ == '__main__':
    main()
