import json
import re
from enum import Enum
from typing import Dict


class SearchField(str, Enum):
    GRAPE = 'grape'
    NAME = 'name'
    COUNTRY = 'country'
    ALCOHOL_CONTENT = 'alcohol_content'
    WINE_TYPE = 'wine_type'


def get_documents_for_query(query: str, field: SearchField):
    with open('inverted_index_without_compression_pairs.json') as pairs_index:
        inverted_index_pairs: Dict = json.load(pairs_index)

    docs = set()
    for key in inverted_index_pairs.keys():
        is_match = re.match(f'.*{query}.*::{field}', key)
        if is_match:
            docs.update(inverted_index_pairs[key])

    if len(docs) != 0:
        return docs

    with open('inverted_index_without_compression_words.json') as words_index:
        inverted_index_words: Dict = json.load(words_index)

    for key in inverted_index_words.keys():
        is_match = re.match(f'.*{query}.*', key)
        if is_match:
            docs.update(inverted_index_words[key])

    return docs


if __name__ == '__main__':
    docs_ = get_documents_for_query('italia', SearchField.COUNTRY)
    print(docs_)
