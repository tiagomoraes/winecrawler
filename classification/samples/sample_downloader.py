import os
import sys
import re
from os import mkdir, path
from concurrent.futures import ThreadPoolExecutor

import requests

IN_FILES = ['/home/borba/Workplace/college/winecrawler/classification/samples/samples_urls.txt', '/home/borba/Workplace/college/winecrawler/classification/samples/nonsamples_urls']
OUT_DIRS = ['../samples/samples_pages', '../samples/nonsamples_pages']


def get_urls(instances: bool) -> [str]:
    in_index = 0 if instances else 1
    with open((IN_FILES[in_index]), 'r') as file:
        # get each url and drop \n at the end
        return [url[:-1] for url in file.readlines()]


def fetch_page(url: str) -> str:
    req = requests.get(url)
    return req.content.decode(encoding='utf-8')


def save_page(content: str, number: int, domain: str, instances: bool):
    out_index = 0 if instances else 1
    file_path = path.join(OUT_DIRS[out_index], 'page-{}-[{}].html'.format(number, domain))
    with open(file_path, 'w') as file:
        file.write(content)


def fetch_save_page(url: str, number: int, instances: bool):
    domain = re.search(r"\.(\w*)\.", url)
    content = fetch_page(url)
    save_page(content, number, domain.group(1), instances)


def download(concurrency: int):
    try:
        mkdir(OUT_DIRS[0])
    except FileExistsError:
        pass
    try:
        mkdir(OUT_DIRS[1])
    except FileExistsError:
        pass

    instances_urls = get_urls(instances=True)
    non_instances_urls = get_urls(instances=False)
    with ThreadPoolExecutor(max_workers=concurrency-1) as executor:
        index = 1
        for url in instances_urls:
            executor.submit(fetch_save_page, url, index, True)
            index += 1
        index = 1
        for url in non_instances_urls:
            executor.submit(fetch_save_page, url, index, False)
            index += 1


if __name__ == '__main__':
    # num_args = len(sys.argv) - 1
    # if num_args != 1:
    #     print('Wrong number of command-line arguments. Expected 1 (concurrency number), received {}'.format(num_args), file=sys.stderr)
    #     sys.exit(1)
    #
    # concurrency = int(sys.argv[1])
    print(os.getcwd())
    download(4)
