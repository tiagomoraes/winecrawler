from bs4 import BeautifulSoup
import requests
import re
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

def has_text(tag):
    text = tag.text.replace('\n', '').strip()
    return text != ''

def global_extract(big_soup):
    try:
        # Reduce the scope to the contents div
        soup = big_soup.find(attrs={'class': re.compile('.*(P|p)roduct.*', re.DOTALL)})

        # If the page has a main tag, the product info tends to be inside
        if soup.main:
            soup = soup.main

        name = None
        name_marker = soup.find(itemprop='name')
        if (name_marker):
            name = name_marker.text.replace('\n', '').strip()

        wine_type = None
        wine_type_marker = soup.find(text=re.compile('.*Tipo.*', re.DOTALL))
        if (wine_type_marker):
            wine_type_sibling = wine_type_marker.find_next(has_text)
            if wine_type_sibling:
                wine_type = wine_type_sibling.text.replace('\n', '').strip()

        grape = None
        grape_marker = soup.find(text=re.compile('.*Uvas?.*', re.DOTALL))
        if (grape_marker):
            grape_sibling = grape_marker.find_next(has_text)
            if grape_sibling:
                grape = grape_sibling.text.replace('\n', '').strip()

        country = None
        country_marker = soup.find(text=re.compile('.*País.*', re.DOTALL))
        if (country_marker):
            country_sibling = country_marker.find_next(has_text)
            if country_sibling:
                country = country_sibling.text.replace('\n', '').strip()

        classification = None
        classification_marker = soup.find(text=re.compile('.*Classificação.*', re.DOTALL))
        if (classification_marker):
            classification_sibling = classification_marker.find_next(has_text)
            if classification_sibling:
                classification = classification_sibling.text.replace('\n', '').strip()

        alcohol_content = None
        alcohol_content_marker = soup.find(text=re.compile('.*(Teor|Graduação).*', re.DOTALL))
        if (alcohol_content_marker):
            alcohol_content_sibling = alcohol_content_marker.find_next(has_text)
            if alcohol_content_sibling:
                alcohol_content = alcohol_content_sibling.text.replace('\n', '').strip()

        year = None
        year_marker = soup.find(text=re.compile('.*Safra.*', re.DOTALL))
        if (year_marker):
            year_sibling = year_marker.find_next(has_text)
            if year_sibling:
                year = year_sibling.text.replace('\n', '').strip()


        return({
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
    domains = ['divinho', 'divvino', 'evino', 'grandcru', 'mistral', 'superadega', 'viavini', 'vinhofacil', 'vivavinho', 'wine']
    for domain in domains:
        extract(domain, global_extract)


if __name__ == '__main__':
    main()