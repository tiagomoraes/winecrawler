import re
import ssl
from extractor import extract, extract_positive_samples, extract_classifier_results

ssl._create_default_https_context = ssl._create_unverified_context


def divvino_extract(soup):
    try:
        name = None
        name_marker = soup.find('h1', itemprop='name')
        if name_marker:
            name = name_marker.text.strip(' ')

        wine_type = None
        wine_type_marker = soup.find('span', text=re.compile('.*Tipo de Vinho.*', re.DOTALL))
        if wine_type_marker:
            wine_type = str(wine_type_marker.parent.find(text=True, recursive=False))

        grape = None
        grape_marker = soup.find('span', text=re.compile('.*Uva.*', re.DOTALL))
        if grape_marker:
            grape = str(grape_marker.parent.find(text=True, recursive=False))

        country = None
        country_marker = soup.find('span', text=re.compile('.*País.*', re.DOTALL))
        if country_marker:
            country = str(country_marker.parent.find(text=True, recursive=False))

        classification = None
        classification_marker = soup.find('span', text=re.compile('.*Classificação.*', re.DOTALL))
        if classification_marker:
            classification = str(classification_marker.parent.find(text=True, recursive=False))

        alcohol_content = None
        alcohol_content_marker = soup.find('span', text=re.compile('.*Teor Alcoólico.*', re.DOTALL))
        if alcohol_content_marker:
            alcohol_content = str(alcohol_content_marker.parent.find(text=True, recursive=False))

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
    # extract('divvino', 'specific', divvino_extract)
    # pages = [52, 57, 68, 113, 124, 255, 310, 394, 488, 604]
    # extract_positive_samples('divvino', pages, divvino_extract)

    extract_classifier_results('divvino', divvino_extract)


if __name__ == '__main__':
    main()
