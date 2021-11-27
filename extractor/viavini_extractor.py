import re
import ssl
from extractor import extract, extract_positive_samples, extract_classifier_results

ssl._create_default_https_context = ssl._create_unverified_context


def viavini_extract(big_soup):
    try:
        soup = big_soup.find('div', attrs={'class': 'datasheet-box'})

        name = None
        name_marker = big_soup.find('span', itemprop="name")
        if name_marker:
            name = name_marker.text

        wine_type = None
        wine_type_marker = big_soup.find('span', attrs={'class': 'tipo-Vinho'})
        if wine_type_marker:
            wine_type = str(wine_type_marker.next).replace(' | ', '')

        grape = None
        grape_marker = soup.find('h6', text=re.compile('.*Uva.*', re.DOTALL))
        if grape_marker:
            grape = grape_marker.findNext('p').text

        country = None
        country_marker = soup.find('div', attrs={'class': 'datasheet-item-text'})
        if country_marker:
            country_new_marker = country_marker.find('h6', attrs={'class': 'attribute-name'})
            if country_new_marker:
                country = country_new_marker.text

        classification = None
        classification_marker = soup.find('h6', text=re.compile('.*Classificação.*', re.DOTALL))
        if classification_marker:
            classification = classification_marker.findNext('p').text

        alcohol_content = None
        alcohol_content_marker = soup.find('h6', text=re.compile('.*Teor.*', re.DOTALL))
        if alcohol_content_marker:
            alcohol_content = alcohol_content_marker.findNext('p').text.replace('°', '%')

        year = None
        year = soup.find('h6', text=re.compile('.*Safra.*', re.DOTALL))
        if year:
            year = year.findNext('p').text

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
    # extract('viavini', 'specific', viavini_extract)
    # pages = [49, 69, 91, 99, 100, 102, 104, 117, 503, 525]
    # extract_positive_samples('viavini', pages, viavini_extract)

    extract_classifier_results('viavini', viavini_extract)


if __name__ == '__main__':
    main()
