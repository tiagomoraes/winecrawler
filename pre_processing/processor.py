import json

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
inverted_index_map = {}


def save_inverted_index(key_value, page_index):
    if inverted_index_map.get(key_value) is None:
        inverted_index_map.setdefault(key_value, [])

    inverted_index_map[key_value].append(page_index)


def save_page_info_inverted_index(page_info, page_index):
    save_inverted_index('{}::name'.format(page_info['name'].lower()), page_index)
    save_inverted_index('{}::grape'.format(page_info['grape'].lower()), page_index)
    save_inverted_index('{}::country'.format(page_info['country'].lower()), page_index)
    save_inverted_index('{}::alcohol_content'.format(page_info['alcohol_content']), page_index)
    save_inverted_index('{}::wine_type'.format(page_info['wine_type'].lower()), page_index)


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

    save_to_file('./inverted_index.json', inverted_index_map)


if __name__ == '__main__':
    create_inverted_index()
