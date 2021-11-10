import ssl
from extractor import extract

ssl._create_default_https_context = ssl._create_unverified_context


def divinho_extract(soup):
    try:
        name = None
        name_marker = soup.find('span', itemprop="name")
        if name_marker:
            name = name_marker.text

        wine_type = None
        wine_type_marker = soup.find('div', attrs={'data-code': 'tipo'})
        if wine_type_marker:
            wine_type = wine_type_marker.text.replace('\n', ' ').strip(' ')

        grape = None
        grape_marker = soup.find('div', attrs={'data-code': 'uva'})
        if grape_marker:
            grape = grape_marker.text.replace('\n', ' ').strip(' ')

        country = None
        country_marker = soup.find('div', attrs={'data-code': 'country_of_manufacture'})
        if country_marker:
            country = country_marker.text.replace('\n', ' ').strip(' ')

        classification = None
        classification_marker = soup.find('div', attrs={'data-code': 'classificacao'})
        if classification_marker:
            classification = classification_marker.text.replace('\n', ' ').strip(' ')

        alcohol_content = None
        alcohol_content_marker = soup.find('div', attrs={'data-code': 'teor_alcoolico'})
        if alcohol_content_marker:
            alcohol_content = alcohol_content_marker.text.replace('\n', ' ').strip(' ')

        year = None
        year_marker = name.split(' ')[-1]
        if year_marker.startswith('1') or year_marker.startswith('2'):
            year = year_marker

        return ({
            'name': name,
            'wine_type': wine_type,
            'grape': grape,
            'country': country,
            'classification': classification,
            'alcohol_content': alcohol_content,
            'year': year,
        })
    except:
        return ({
            'name': '',
            'wine_type': '',
            'grape': '',
            'country': '',
            'classification': '',
            'alcohol_content': '',
            'year': '',
        })


def main():
    extract('divinho', divinho_extract)


if __name__ == '__main__':
    main()
