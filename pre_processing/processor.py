import json
import unidecode
from classification.helpers.corpus_loader import load_corpus_from

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


def normalize_string(s: str) -> str:
    return unidecode.unidecode(s.lower().strip())\
        .replace('!', '')\
        .replace('@', '')\
        .replace('#', '')\
        .replace('$', '') \
        .replace('%', '') \
        .replace('^', '')\
        .replace('&', '')\
        .replace('*', '')\
        .replace('(', '')\
        .replace(')', '')


def get_alcohol_content_interval(alcohol_content: str) -> int:
    terms = alcohol_content.split(',')
    value = 0.0
    if len(terms) > 1:
        value = float(terms[0]) + float('0.'+terms[1][0])
    else:
        value = float(normalize_string(terms[0]))

    if value < 5:
        return 0

    if value < 10:
        return 1

    if value < 15:
        return 2

    return 3


def save_page_info_inverted_index(page_info, page_index):
    name = normalize_string(page_info['name'])
    grape = normalize_string(page_info['grape'])
    country = normalize_string(page_info['country'])
    alcohol_content = str(get_alcohol_content_interval(page_info['alcohol_content']))
    wine_type = normalize_string(page_info['wine_type'])

    save_inverted_index_with_compression('{}::name'.format(name), page_index)
    save_inverted_index_with_compression('{}::grape'.format(grape), page_index)
    save_inverted_index_with_compression('{}::country'.format(country), page_index)
    save_inverted_index_with_compression('{}::alcohol_content'.format(alcohol_content), page_index)
    save_inverted_index_with_compression('{}::wine_type'.format(wine_type), page_index)

    save_inverted_index_without_compression('{}::name'.format(name), page_index)
    save_inverted_index_without_compression('{}::grape'.format(grape), page_index)
    save_inverted_index_without_compression('{}::country'.format(country), page_index)
    save_inverted_index_without_compression('{}::alcohol_content'.format(alcohol_content), page_index)
    save_inverted_index_without_compression('{}::wine_type'.format(wine_type), page_index)


def save_to_file(path, data):
    results_file = open(path, 'w')
    results_file.write(json.dumps(data))


def create_inverted_index_from_extractors():
    for domain in domains:
        f = open('../extractor/results/logistic_classifier/{}.json'.format(domain))

        data_results = json.load(f)
        for result in data_results:
            for key in result.keys():
                if result[key] is not None:
                    page_info = result[key]
                    save_page_info_inverted_index(page_info, key)
    # print(sys.getsizeof(inverted_index_map))
    # np.uint16 -> 73816
    # str -> 73816
    # int -> 73816


def create_inverted_index_from_words():
    for index in range(10000):
        try:
            corpus = load_corpus_from('../extractor/pages/{}.html'.format(index)).drop_stop_words()
            for token in corpus.vocabulary:
                save_inverted_index_with_compression(normalize_string(token), index)
                save_inverted_index_without_compression(normalize_string(token), index)
        except:
            pass


def create_inverted_index():
    create_inverted_index_from_extractors()
    save_to_file('./inverted_index_with_compression_pairs.json', inverted_index_map_with_compression)
    save_to_file('./inverted_index_without_compression_pairs.json', inverted_index_map_without_compression)

    # reset inverted indexes
    inverted_index_map_with_compression.clear()
    inverted_index_map_without_compression.clear()

    create_inverted_index_from_words()
    save_to_file('./inverted_index_with_compression_words.json', inverted_index_map_with_compression)
    save_to_file('./inverted_index_without_compression_words.json', inverted_index_map_without_compression)


if __name__ == '__main__':
    create_inverted_index()
