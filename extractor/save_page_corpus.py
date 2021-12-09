import json
from os import listdir
from os.path import isfile, join

from classification.helpers.corpus_loader import load_corpus_from


def save_page_corpus():
    result = {}
    dir_path = 'pages/'
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    for file in files:
        file_corpus = load_corpus_from(f'{dir_path}{file}').drop_stop_words()
        result[file.replace('.html', '')] = file_corpus.to_json()

    with open('pages_corpus/loaded_page_corpus.json', 'w') as file:
        file.write(json.dumps(result))


if __name__ == '__main__':
    save_page_corpus()
