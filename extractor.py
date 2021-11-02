from bs4 import BeautifulSoup
import requests
import re
import ssl
from time import sleep
import csv

ssl._create_default_https_context = ssl._create_unverified_context

def wine_extract(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')

    grape = soup.find(text=re.compile('.*Uva.*', re.DOTALL)).parent.find_next('dd').text
    country = soup.find(text=re.compile('.*País.*', re.DOTALL)).parent.find_next('dd').text
    classification = soup.find(text=re.compile('.*Classificação.*', re.DOTALL)).parent.find_next('dd').text
    year = soup.find(text=re.compile('.*Safra.*', re.DOTALL)).parent.find_next('dd').text
    alcohol_content = soup.find(text=re.compile('.*Teor.*', re.DOTALL)).parent.find_next('dd').text
    

def main():
    wine_extract('https://www.wine.com.br/vinhos/370-leguas-doc-douro-2019/prod25238.html?channable=0163e4696400323532333821&utm_source=blue&utm_medium=rtg-loja&utm_campaign=retargetingblue')

if __name__ == '__main__':
    main()