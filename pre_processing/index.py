import itertools
import json
import re
from enum import Enum
from typing import Dict, List
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


# normal: dict_keys([5989, 7205, 7033, 7100, 4119, 5210, 1116, 5212, 5216, 5218, 5957, 5026, 5046, 4636, 4641, 1186, 4785, 228, 5887, 4376, 4443, 4973, 6, 4108, 36, 4651, 584, 4170, 590, 4174, 593, 594, 5200, 5211, 4192, 5217, 5221, 5223, 5226, 5228, 5247, 149, 4767, 5294, 5297, 182, 190, 4809, 5330, 5332, 5334, 4832, 4330, 4843, 5354, 256, 265, 267, 272, 282, 4381, 5928, 5929, 818, 5958, 1358, 851, 5997, 5035, 5043, 4534, 5098, 4681, 4172, 4684, 4206, 4213, 4215, 4825, 4478, 4530, 4123, 4659, 4700, 4773, 4371, 836, 6989, 4449, 4175, 4770, 4774, 4833, 4847, 4337, 4340, 4378, 6445, 4445, 4541, 4552, 4095, 4114, 4705, 4727, 4813, 4834, 4428, 4538, 1009, 2080, 2587, 2608, 2101, 3149, 2742, 3344, 2565, 2578, 2581, 3105, 2083, 2601, 2604, 2605, 2606, 2607, 2096, 2099, 2612, 2102, 2127, 2698, 2722, 2215, 2225, 2740, 2743, 2757, 2764, 2767, 2261, 2271, 2279, 2282, 2315, 3347, 3348, 2411, 2415, 2418, 2426, 2429, 2432, 3517, 3531])
# tfidf: dict_keys([1116, 1186, 1358, 1009, 265, 267, 272, 282, 584, 590, 593, 594, 818, 836, 6, 182, 256, 36, 228, 149, 190, 851, 7100, 7033, 7205, 4174, 4192, 4534, 4825, 4651, 4641, 4785, 4376, 4767, 4809, 4330, 4843, 4973, 4114, 4381, 4684, 4378, 4371, 4175, 4770, 4774, 4337, 4445, 4541, 4552, 4095, 4538, 4172, 4700, 4832, 4833, 4443, 4847, 4340, 4123, 4659, 4773, 4813, 4449, 4681, 4478, 4119, 4834, 4428, 4636, 4530, 4170, 4705, 4213, 5957, 4206, 4215, 4108, 4727, 5989, 5210, 5216, 5043, 5297, 5046, 5098, 6445, 5928, 6989, 5958, 5997, 5200, 5212, 5218, 5221, 5247, 5294, 5354, 5929, 5026, 5887, 5211, 5217, 5223, 5226, 5228, 5330, 5332, 5334, 5035, 2698, 2080, 2587, 2608, 2101, 2742, 2565, 2578, 2581, 2083, 2601, 2604, 2605, 2606, 2607, 2096, 2099, 2612, 2102, 2127, 2722, 2215, 2225, 2740, 2743, 2757, 2764, 2767, 2261, 2271, 2279, 2282, 2315, 2411, 2415, 2418, 2426, 2429, 2432, 3517, 3344, 3531, 3149, 3105, 3347, 3348])
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
    number_of_documents = len(production_rank)
    k = number_of_documents * (number_of_documents - 1)

    ordered_pair_docs_production_rank.intersection(ordered_pair_docs_new_rank)

    correlation = 1 - (k - len(ordered_pair_docs_new_rank))/k
    return correlation


if __name__ == '__main__':
    docs_ = get_documents_for_query('italia', SearchField.COUNTRY)
    # docs_ = get_documents_for_query('vinho tinto', SearchField.NAME)
    # docs_ = get_documents_for_query('syrah', SearchField.GRAPE)
    # docs_ = get_documents_for_query('branco', SearchField.WINE_TYPE)
    # docs_ = get_documents_for_query('16,5%', SearchField.ALCOHOL_CONTENT)
    positive_docs_len = len(dict(filter(lambda x: x[1] > 0, docs_.items())).keys())

    result_normal = list(dict(sorted(docs_.items(), key=lambda x: x[1], reverse=True)).keys())
    result_tfidf = list(dict(sorted(docs_.items(), key=lambda x: calculate_tf_idf(x[1], positive_docs_len, x[0]), reverse=True)).keys())

    print(result_normal)
    print(result_tfidf)
    
    spearman_correlation = calculate_spearman_correlation(result_normal, result_tfidf)
    print(spearman_correlation)
    kendal_tau_correlation = calculate_kendal_tau_correlation(result_normal, result_tfidf)
    print(kendal_tau_correlation)

