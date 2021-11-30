import json
import sys

import numpy as np

domains = [
    'adegamais',
    'divinho',
    'divvino',
    'evino',
    'grandcru',
    'mistral',
    'superadega',
    'viavini',
    'vivavinho',
    'wine'
]
inverted_index_map_with_compression = {}
inverted_index_map_without_compression = {}


def save_inverted_index_with_compression(key_value, page_index):
    if inverted_index_map_with_compression.get(key_value) is None:
        inverted_index_map_with_compression.setdefault(key_value, [])

    index_sum = 0
    for element in inverted_index_map_with_compression.get(key_value):
        index_sum += element

    diff = int(page_index) - index_sum
    inverted_index_map_with_compression[key_value].append(diff)


def save_inverted_index_without_compression(key_value, page_index):
    if inverted_index_map_without_compression.get(key_value) is None:
        inverted_index_map_without_compression.setdefault(key_value, [])

    inverted_index_map_without_compression[key_value].append(int(page_index))


def save_page_info_inverted_index(page_info, page_index):
    save_inverted_index_with_compression('{}::name'.format(page_info['name'].lower()), page_index)
    save_inverted_index_with_compression('{}::grape'.format(page_info['grape'].lower()), page_index)
    save_inverted_index_with_compression('{}::country'.format(page_info['country'].lower()), page_index)
    save_inverted_index_with_compression('{}::alcohol_content'.format(page_info['alcohol_content']), page_index)
    save_inverted_index_with_compression('{}::wine_type'.format(page_info['wine_type'].lower()), page_index)

    save_inverted_index_without_compression('{}::name'.format(page_info['name'].lower()), page_index)
    save_inverted_index_without_compression('{}::grape'.format(page_info['grape'].lower()), page_index)
    save_inverted_index_without_compression('{}::country'.format(page_info['country'].lower()), page_index)
    save_inverted_index_without_compression('{}::alcohol_content'.format(page_info['alcohol_content']), page_index)
    save_inverted_index_without_compression('{}::wine_type'.format(page_info['wine_type'].lower()), page_index)


def save_to_file(path, data):
    results_file = open(path, 'w')
    results_file.write(json.dumps(data))


def create_inverted_index():
    for domain in domains:
        f = open('../extractor/results/logistic_classifier/{}.json'.format(domain))

        data_results = json.load(f)
        for result in data_results:
            for key in result.keys():
                if result[key] is not None:
                    page_info = result[key]
                    save_page_info_inverted_index(page_info, key)

    save_to_file('./inverted_index_with_compression.json', inverted_index_map_with_compression)
    save_to_file('./inverted_index_without_compression.json', inverted_index_map_without_compression)
    # print(sys.getsizeof(inverted_index_map))
    # np.uint16 -> 73816
    # str -> 73816
    # int -> 73816


if __name__ == '__main__':
    create_inverted_index()
