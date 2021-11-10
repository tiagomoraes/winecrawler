import re
import ssl
from extractor import extract

ssl._create_default_https_context = ssl._create_unverified_context


def adegamais_extract(soup):
    try:
        name = None
        name_marker = soup.find('h1', attrs={'class': 'product-title'})
        if (name_marker):
            name = name_marker.text

        wine_type = None
        wine_type_marker = soup.find('strong', text=re.compile('.*Tipo.*', re.DOTALL))
        if (wine_type_marker):
            wine_type = wine_type_marker.find_next('p').text.strip(' ')

        grape = None
        grape_marker = soup.find('strong', text=re.compile('.*Uva.*', re.DOTALL))
        if (grape_marker):
            grape = grape_marker.find_next('p').text.strip(' ')

        country = None
        country_marker = soup.find('strong', text=re.compile('.*País.*', re.DOTALL))
        if (country_marker):
            country = country_marker.find_next('p').text.strip(' ')

        classification = None
        classification_marker = soup.find('strong', text=re.compile('.*Classificação.*', re.DOTALL))
        if (classification_marker):
            classification = classification_marker.find_next('p').text.strip(' ')

        alcohol_content = None
        alcohol_content_marker = soup.find('strong', text=re.compile('.*Teor Alcoólico.*', re.DOTALL))
        if (alcohol_content_marker):
            alcohol_content = alcohol_content_marker.find_next('p').text.strip(' ')

        year = None
        year_marker = soup.find('strong', text=re.compile('.*Safra.*', re.DOTALL))
        if (year_marker):
            year = year_marker.find_next('p').text.strip(' ')

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
    extract('adegamais', 'specific', adegamais_extract)


if __name__ == '__main__':
    main()
