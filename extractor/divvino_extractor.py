from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


def divvino_extract(soup):
    name = None
    name_marker = soup.find('h1', itemprop='name')
    if name_marker:
        name = name_marker.text.strip(' ')

    wine_type = None
    wine_type_marker = soup.find('span', text=re.compile('.*Tipo de Vinho.*', re.DOTALL))
    if wine_type_marker:
        wine_type = wine_type_marker.parent.find(text=True, recursive=False).text

    grape = None
    grape_marker = soup.find('span', text=re.compile('.*Uva.*', re.DOTALL))
    if grape_marker:
        grape = grape_marker.parent.find(text=True, recursive=False).text

    country = None
    country_marker = soup.find('span', text=re.compile('.*País.*', re.DOTALL))
    if country_marker:
        country = country_marker.parent.find(text=True, recursive=False).text

    classification = None
    classification_marker = soup.find('span', text=re.compile('.*Classificação.*', re.DOTALL))
    if classification_marker:
        classification = classification_marker.parent.find(text=True, recursive=False).text

    alcohol_content = None
    alcohol_content_marker = soup.find('span', text=re.compile('.*Teor Alcoólico.*', re.DOTALL))
    if alcohol_content_marker:
        alcohol_content = alcohol_content_marker.parent.find(text=True, recursive=False).text

    year = None
    year_marker = soup.find('p', attrs={'class': 'clear subtitle'})
    if year_marker:
        year_temp = year_marker.text.split('|')[0]
        if year_temp.startswith('1') or year_temp.startswith('2'):
            year = year_temp.replace('\xa0', '')

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
    html = requests.get('https://www.divvino.com.br/p/vinho-tinto-portugues-cavalo-bravo-4194771')
    soup = BeautifulSoup(html.text, 'html.parser')

    print(divvino_extract(soup))


if __name__ == '__main__':
    main()
