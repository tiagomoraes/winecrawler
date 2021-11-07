from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def mistral_extract(soup):
    name = None
    name_marker = soup.find('h1', attrs={'class': 'name-wine-product-new'})
    if (name_marker):
        name = name_marker.text

    wine_type = None
    wine_type_marker = soup.find('p', text=re.compile('.*Tipo.*', re.DOTALL))
    if (wine_type_marker):
        wine_type = wine_type_marker.findNext('p').text

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
    html = requests.get('')
    soup = BeautifulSoup(html.text, 'html.parser')

    print(mistral_extract(soup))


if __name__ == '__main__':
    main()
