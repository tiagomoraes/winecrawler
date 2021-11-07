from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def evino_extract(soup):
    name = None
    name_marker = soup.find('h2', itemprop='name')
    if (name_marker):
        name = name_marker.text

    wine_type = None
    wine_type_marker = soup.find('h4', text=re.compile('.*Tipo.*', re.DOTALL))
    if (wine_type_marker):
        wine_type = wine_type_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text

    grape = None
    grape_marker = soup.find('h4', text=re.compile('.*Uva.*', re.DOTALL))
    if (grape_marker):
        grape = grape_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text

    country = None
    country_marker = soup.find('h4', text=re.compile('.*País.*', re.DOTALL))
    if (country_marker):
        country = country_marker.parent.find_next('span', attrs={'class': 'TruncateText__content'}).text

    classification = None
    classification_marker = soup.find(lambda tag: tag.name == 'h4' and 'Classificação' in tag.text)
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
    html = requests.get('https://www.evino.com.br/product/alcanta-white-2020-241351.html')
    soup = BeautifulSoup(html.text, 'html.parser')

    print(evino_extract(soup))


if __name__ == '__main__':
    main()
