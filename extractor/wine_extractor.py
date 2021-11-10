import re
import ssl

from extractor import extract

ssl._create_default_https_context = ssl._create_unverified_context


def wine_extract(soup):
    try:
        name = None
        name_marker = soup.find('h1', attrs={'class': 'PageHeader-title'})
        if name_marker:
            name = name_marker.text

        wine_type = None
        wine_type_marker = soup.find(text=re.compile('.*Tipo.*', re.DOTALL))
        if wine_type_marker:
            wine_type = wine_type_marker.parent.find_next('dd').text

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
    extract('wine', wine_extract)


if __name__ == '__main__':
    main()
