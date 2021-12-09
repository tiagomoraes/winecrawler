import itertools
import json
import re
from enum import Enum
from os import listdir
from os.path import isfile, join
from typing import Dict, List, Optional
import numpy as np
from types import SimpleNamespace

from pydantic import BaseModel

from classification.helpers.corpus import Corpus
from classification.helpers.corpus_loader import load_corpus_from
from pre_processing.processor import get_alcohol_content_interval


class SearchField(str, Enum):
    GRAPE = 'grape'
    NAME = 'name'
    COUNTRY = 'country'
    ALCOHOL_CONTENT = 'alcohol_content'
    WINE_TYPE = 'wine_type'


class SingleDocInformation(BaseModel):
    name: Optional[str]
    wine_type: Optional[str]
    grape: Optional[str]
    country: Optional[str]
    classification: Optional[str]
    alcohol_content: Optional[str]
    year: Optional[str]


class SearchResponse(BaseModel):
    total_number_of_docs: int
    has_next_page: bool
    docs_information: Dict[int, SingleDocInformation]


TOTAL_DOCUMENTS = 3918

documents_page = {
    974: 'adegamais', 1994: 'divinho', 2978: 'divvino', 3989: 'evino', 4999: 'grandcru', 6000: 'mistral',
    7000: 'superadega', 7994: 'viavini', 8998: 'vivavinho', 9987: 'wine'
}


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
    return np.log((1 + TOTAL_DOCUMENTS) / (1 + total_positive_documents))


def get_tf(frequency: int, most_frequent: int) -> float:
    return 0.5 + (0.5 * frequency) / 1 + most_frequent


def calculate_tf_idf(frequency: int, total_positive_documents: int, page_index: int) -> float:
    most_frequent_occurrence = get_most_frequent_value(page_index)
    return get_tf(frequency, most_frequent_occurrence) * get_idf(total_positive_documents)


def get_documents_for_query(query: str, field: SearchField):
    docs = set()
    tokens = query.split(' ')
    if field == SearchField.ALCOHOL_CONTENT:
        query = get_alcohol_content_interval(query)

    with open(f'../pre_processing/inverted_index_without_compression_pairs.json') as pairs_index:
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

    # if did not find pairs, search in words index
    if len(docs) == 0:
        with open(f'../pre_processing/inverted_index_without_compression_words.json') as words_index:
            inverted_index_words: Dict = json.load(words_index)

            for token in tokens:
                docs_indices = inverted_index_words.get(token, None)
                if docs_indices is not None:
                    docs.update(docs_indices)

    frequencies_per_doc = {}
    for index, doc in enumerate(docs):
        sum_frequencies = 0
        for token in tokens:
            token_frequency = get_token_frequency(token, doc)
            sum_frequencies += token_frequency

        frequencies_per_doc.setdefault(doc, sum_frequencies)

    return frequencies_per_doc


def calculate_spearman_correlation(production_rank: List[int], new_rank: List[int]):
    k = len(production_rank)
    sum_square_distances = 0
    for i, doc in enumerate(production_rank):
        new_rank_index = new_rank.index(doc)
        curr_correlation = i - new_rank_index
        sum_square_distances += curr_correlation*curr_correlation

    correlation = 1 - (6 * sum_square_distances)/(k * (k*k - 1))
    return correlation


def calculate_kendal_tau_correlation(production_rank: List[int], new_rank: List[int]):
    ordered_pair_docs_production_rank = set(itertools.combinations(production_rank, 2))
    ordered_pair_docs_new_rank = set(itertools.combinations(new_rank, 2))
    k = len(production_rank)

    symmetric_difference_size = len(ordered_pair_docs_production_rank ^ ordered_pair_docs_new_rank)

    correlation = 1 - (2*symmetric_difference_size)/(k * (k - 1))
    return correlation


def rank_documents(docs: Dict, use_td_idf: bool = False):
    if use_td_idf:
        positive_docs_len = len(dict(filter(lambda x: x[1] > 0, docs.items())).keys())
        result = sorted(docs.items(), key=lambda x: calculate_tf_idf(x[1], positive_docs_len, x[0]), reverse=True)
    else:
        result = sorted(docs.items(), key=lambda x: x[1], reverse=True)

    return list(dict(result).keys())


def find_document_domain(doc_index: int) -> Optional[str]:
    for page_index in documents_page:
        if doc_index < page_index:
            return documents_page[page_index]
    return None


def __paginate(list_: List, page_size: int, page: int):
    from_ = (page - 1) * page_size
    to = from_ + page_size
    return list_[from_:to]


def has_next_page(list_length: int, page_size: int, page: int):
    actual = page * page_size
    return actual < list_length


def retrieve_docs_information(docs: List, page_size: int, page: int):
    result = {}
    for doc in __paginate(docs, page_size, page):
        doc_page = find_document_domain(doc)
        if doc_page is None:
            return
        with open(f'../extractor/results/logistic_classifier/{doc_page}_indexed.txt', 'r') as file:
            indexes: Dict = json.load(file)
            wine_info = indexes.get(str(doc), None)
            if wine_info is not None:
                result[doc] = wine_info
    return result


def parse_logistic_classifier_results_to_dict():
    dir_path = '../extractor/results/logistic_classifier/'
    files = [f for f in listdir(dir_path) if isfile(join(dir_path, f))]
    for file in files:
        with open(f'{dir_path}{file}', 'r') as curr_file:
            result_dict = {}
            parsed_json = (json.load(curr_file))
            for index in parsed_json:
                doc_index = list(index.keys())[0]
                result_dict[doc_index] = index[doc_index]
            with open(f"{dir_path}{file.replace('.json', '')}_indexed.txt", 'w') as indexed_file:
                indexed_file.write(json.dumps(result_dict))


def mocked_query_to_calculate_correlation_sample():
    queries = [('italia', SearchField.COUNTRY), ('vinho tinto', SearchField.NAME), ('syrah', SearchField.GRAPE),
               ('branco', SearchField.WINE_TYPE), ('16,5%', SearchField.ALCOHOL_CONTENT)]
    for query in queries:
        docs = get_documents_for_query(query[0], query[1])
        normal_rank = rank_documents(docs)
        tf_idf_rank = rank_documents(docs, True)
        spearman_correlation = calculate_spearman_correlation(normal_rank, tf_idf_rank)
        kendal_tau_correlation = calculate_kendal_tau_correlation(normal_rank, tf_idf_rank)
        print(f"{query[0]}, {query[1]}, {spearman_correlation}, {kendal_tau_correlation}")


if __name__ == '__main__':
    mocked_query_to_calculate_correlation_sample()

