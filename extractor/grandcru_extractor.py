from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def grandcru_extract(soup):
    name = None
    name_marker = soup.find('h1', attrs={'class': 'product-title'})
    if (name_marker):
        name = name_marker.find('span').text.replace('\n', '').strip(' ')

    wine_type = None
    wine_type_marker = soup.find('span', attrs={'class': 'tipo-vinho'})
    if (wine_type_marker):
        wine_type = wine_type_marker.find('small').text

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

    print(grandcru_extract(soup))


if __name__ == '__main__':
    main()
