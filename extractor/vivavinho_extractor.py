import re
import ssl
from extractor import extract, extract_positive_samples, extract_classifier_results

ssl._create_default_https_context = ssl._create_unverified_context

def vivavinho_extract(soup):
    try:
        name = None
        name_marker = soup.find('div', attrs={'class': 'productName'})
        if (name_marker):
            name = name_marker.text

        wine_type = None
        wine_type_marker = soup.find('td', attrs={'class': 'value-field Tipo'})
        if (wine_type_marker):
            wine_type = wine_type_marker.text

        grape = None
        grape_marker = soup.find('td', attrs={'class': 'value-field Uva'})
        if (grape_marker):
            grape = grape_marker.text

        country = None
        country_marker = soup.find('td', attrs={'class': 'value-field Pais'})
        if (country_marker):
            country = country_marker.text

        classification = None
        classification_marker = soup.find('td', attrs={'class': 'value-field Classificacao'})
        if (classification_marker):
            classification = classification_marker.text

        alcohol_content = None
        alcohol_content_marker = soup.find('td', attrs={'class': 'value-field Graduacao-alcoolica'})
        if (alcohol_content_marker):
            alcohol_content = alcohol_content_marker.text

        year = None
        year_marker = soup.find('td', attrs={'class': 'value-field Safra'})
        if (year_marker):
            year = year_marker.text

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
    # extract('vivavinho', 'specific', vivavinho_extract)
    # pages = [61, 160, 166, 167, 177, 252, 255, 331, 349, 738]
    # extract_positive_samples('vivavinho', pages, vivavinho_extract)

    extract_classifier_results('vivavinho', vivavinho_extract)


if __name__ == '__main__':
    main()
