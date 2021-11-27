import re
import ssl
from extractor import extract, extract_positive_samples, extract_classifier_results

ssl._create_default_https_context = ssl._create_unverified_context


def mistral_extract(soup):
    try:
        name = None
        name_marker = soup.find('h1', attrs={'class': 'name-wine-product-new'})
        if (name_marker):
            name = str(name_marker.text).replace('\n', '').strip()

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
    # extract('mistral', 'specific', mistral_extract)
    # pages = [12, 19, 85, 137, 205, 244, 418, 440, 456, 861]
    # extract_positive_samples('mistral', pages, mistral_extract)
    extract_classifier_results('mistral', mistral_extract)


if __name__ == '__main__':
    main()
