import glob
import json

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
                save_inverted_index_with_compression(token.lower(), index)
                save_inverted_index_without_compression(token.lower(), index)
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
