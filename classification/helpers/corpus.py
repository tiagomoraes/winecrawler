import json
from typing import List

from nltk.corpus import stopwords as nltk_stopwords
import nltk
from pydantic import BaseModel

from classification.helpers.document import DocumentClass, Document

nltk.download('stopwords')


class CorpusTokenStats:
    def __init__(self):
        self.data = {
            DocumentClass.INSTANCE.value: {
                'freq': 0,
                'docs': [],
            },
            DocumentClass.NON_INSTANCE.value: {
                'freq': 0,
                'docs': [],
            },
        }

    def add_stats(self, freq: int, doc: int, is_instance: DocumentClass):
        self.data[is_instance.value]['freq'] += freq
        self.data[is_instance.value]['docs'].append(doc)

    def get_total_freq(self) -> int:
        return self.data[DocumentClass.INSTANCE.value]['freq'] + self.data[DocumentClass.NON_INSTANCE.value]['freq']

    def get_all_docs(self) -> [int]:
        return self.data[DocumentClass.INSTANCE.value]['docs'] + self.data[DocumentClass.NON_INSTANCE.value]['docs']


class Corpus(BaseModel):
    def __init__(self, documents: List[Document]):
        super(Corpus, self).__init__()
        self.documents = documents
        self.__build_corpus_vocabulary()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __build_corpus_vocabulary(self):
        self.vocabulary = {}
        stemmer = nltk.stem.porter.PorterStemmer()

        for i, document in enumerate(self.documents):
            for token in document.vocabulary:
                freq = document.vocabulary[token]

                lower_token = token.lower()
                stemmed_lower_token = stemmer.stem(lower_token)

                stats = self.vocabulary.get(stemmed_lower_token, None)
                if stats is None:
                    self.vocabulary[stemmed_lower_token] = CorpusTokenStats()

                self.vocabulary[stemmed_lower_token].add_stats(freq, i, document.is_instance)

    def drop_stop_words(self, in_place: bool = True):
        return_corpus = self
        if not in_place:
            return_corpus = Corpus(self.documents)

        for stop_word in nltk_stopwords.words('portuguese'):
            try:
                del return_corpus.vocabulary[stop_word]
            except KeyError:
                pass

        return return_corpus

    def vocabulary_get(self, word: str) -> CorpusTokenStats:
        stats = self.vocabulary.get(word, None)
        if stats is None:
            self.vocabulary[word] = CorpusTokenStats()
        return self.vocabulary[word]


if __name__ == '__main__':
    doc_1 = Document.load_from_url('https://www.vivavinho.com.br/vinho-rose-italiano-wave-rosato-igt-750ml/p', DocumentClass.INSTANCE)
    doc_2 = Document.load_from_url('https://www.vivavinho.com.br/vinho-branco-italiano-wave-bianco-igt-750ml/p', DocumentClass.INSTANCE)
    doc_3 = Document.load_from_url('https://www.vivavinho.com.br/vinho-rose-portugues-5-elementos-750ml/p', DocumentClass.INSTANCE)
    corpus = Corpus([doc_1, doc_2, doc_3])
    print(corpus.documents)
    print(corpus.vocabulary)
    for token in corpus.vocabulary:
        occurrences = len(corpus.vocabulary[token].get_all_docs())
        total_docs = len(corpus.documents)
        if total_docs * .4 < occurrences:
            print("{} = {}".format(token, occurrences))
