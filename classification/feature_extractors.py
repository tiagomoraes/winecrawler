from abc import ABC, abstractmethod
from typing import Callable

import nltk

from classification.helpers.corpus import Corpus
from classification.helpers.document import DocumentClass


class FeatureExtractor(ABC):
    def __init__(self, corpus: Corpus):
        super().__init__()
        self.corpus = corpus
        self.stemmer = nltk.stem.porter.PorterStemmer()

    @abstractmethod
    def _word_cmp_key(self) -> Callable[[str], int]:
        pass

    def get_feature_words(self, num_features: int = 30) -> [str]:
        return sorted(self.corpus.vocabulary, key=self._word_cmp_key(), reverse=True)[:num_features]


class MostFrequentWordsExtractor(FeatureExtractor):
    def __init__(self, corpus: Corpus):
        super().__init__(corpus)

    def _word_cmp_key(self) -> Callable[[str], int]:
        return lambda word: self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).get_total_freq()


class DocFrequencyDifferenceExtractor(FeatureExtractor):
    def __init__(self, corpus: Corpus):
        super().__init__(corpus)

    def _word_cmp_key(self) -> Callable[[str], int]:
        return (lambda word: abs(
            len(self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).data[DocumentClass.INSTANCE.value]['docs'])
            - len(self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).data[DocumentClass.NON_INSTANCE.value][
                      'docs'])))


class PlainFrequencyDifferenceExtractor(FeatureExtractor):
    def __init__(self, corpus: Corpus):
        super().__init__(corpus)

    def _word_cmp_key(self) -> Callable[[str], int]:
        return (lambda word: abs(
            self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).data[DocumentClass.INSTANCE.value]['freq']
            - self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).data[DocumentClass.NON_INSTANCE.value][
                'freq']))


class MixedFrequencyDifferenceExtractor(FeatureExtractor):
    def __init__(self, corpus: Corpus):
        super().__init__(corpus)

    def _word_cmp_key(self) -> Callable[[str], int]:
        return (lambda word: (abs(len(
            self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).data[DocumentClass.INSTANCE.value][
                'docs']) - len(
            self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).data[DocumentClass.NON_INSTANCE.value][
                'docs'])) + 1) * (abs(
            self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).data[DocumentClass.INSTANCE.value]['freq'] -
            self.corpus.vocabulary_get(self.stemmer.stem(word).lower()).data[DocumentClass.NON_INSTANCE.value][
                'freq']) + 1))
