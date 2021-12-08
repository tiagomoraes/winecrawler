import json
import re
from enum import Enum
from typing import Dict
import numpy as np

from classification.helpers.corpus_loader import load_corpus_from
from pre_processing.processor import get_alcohol_content_interval


class SearchField(str, Enum):
    GRAPE = 'grape'
    NAME = 'name'
    COUNTRY = 'country'
    ALCOHOL_CONTENT = 'alcohol_content'
    WINE_TYPE = 'wine_type'


TOTAL_DOCUMENTS = 3918
# TOTAL_DOCUMENTS = 10


def get_token_frequency(token: str, page_index: int) -> int:
    corpus = load_corpus_from('../extractor/pages/{}.html'.format(page_index)).drop_stop_words()
    if token in corpus.vocabulary:
        return corpus.vocabulary[token].get_total_freq()

    return 0


def get_most_frequent_value(page_index: int) -> int:
    corpus = load_corpus_from('../extractor/pages/{}.html'.format(page_index)).drop_stop_words()
    most_frequent_value = -1
    for word in corpus.vocabulary:
        word_frequency = corpus.vocabulary[word].get_total_freq()
        if word_frequency > most_frequent_value:
            most_frequent_value = word_frequency

    return most_frequent_value


def get_idf(total_positive_documents: int) -> float:
    return np.log((1+TOTAL_DOCUMENTS) / (1+total_positive_documents))


def get_tf(frequency: int, most_frequent: int) -> float:
    return 0.5 + (0.5 * frequency)/1+most_frequent


def calculate_tf_idf(frequency: int, total_positive_documents: int, page_index: int) -> float:
    most_frequent_occurrence = get_most_frequent_value(page_index)
    return get_tf(frequency, most_frequent_occurrence) * get_idf(total_positive_documents)


def get_documents_for_query(query: str, field: SearchField):
    docs = set()
    tokens = query.split(' ')
    if field == SearchField.ALCOHOL_CONTENT:
        query = get_alcohol_content_interval(query)

    with open('inverted_index_without_compression_pairs.json') as pairs_index:
        inverted_index_pairs: Dict = json.load(pairs_index)
        for key in inverted_index_pairs.keys():
            is_match = re.match(f'.*{query}.*::{field}', key)
            if is_match:
                docs.update(inverted_index_pairs[key])

        for key in inverted_index_pairs.keys():
            for token in tokens:
                is_match = re.match(f'.*{token}.*::{field}', key)
                if is_match:
                    docs.update(inverted_index_pairs[key])

    # if didnt find pairs, search in words index
    if len(docs) == 0:
        with open('inverted_index_without_compression_words.json') as words_index:
            inverted_index_words: Dict = json.load(words_index)

            for key in inverted_index_words.keys():
                is_match = re.match(f'.*{query}.*', key)
                if is_match:
                    docs.update(inverted_index_words[key])

            for key in inverted_index_words.keys():
                for token in tokens:
                    is_match = re.match(f'.*{token}.*', key)
                    if is_match:
                        docs.update(inverted_index_words[key])

    frequencies_per_doc = {}
    for index, doc in enumerate(docs):
        sum_frequencies = 0
        for token in tokens:
            token_frequency = get_token_frequency(token, doc)
            sum_frequencies += token_frequency

        frequencies_per_doc.setdefault(doc, sum_frequencies)

    return frequencies_per_doc


if __name__ == '__main__':
    docs_ = get_documents_for_query('italia', SearchField.COUNTRY)
    # docs_ = get_documents_for_query('vinho tinto', SearchField.NAME)
    # docs_ = get_documents_for_query('syrah', SearchField.GRAPE)
    # docs_ = get_documents_for_query('branco', SearchField.WINE_TYPE)
    # docs_ = get_documents_for_query('16,5%', SearchField.ALCOHOL_CONTENT)
    positive_docs_len = len(dict(filter(lambda x: x[1] > 0, docs_.items())).keys())

    result_normal = dict(sorted(docs_.items(), key=lambda x: x[1], reverse=True)).keys()
    result_tfidf = dict(sorted(docs_.items(), key=lambda x: calculate_tf_idf(x[1], positive_docs_len, x[0]), reverse=True)).keys()

    print(result_normal)
    print(result_tfidf)
