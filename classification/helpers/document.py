import enum
from typing import List

from bs4 import BeautifulSoup
import nltk
import requests

from classification.helpers.tokenize import tokenize


class DocumentClass(enum.IntEnum):
    NON_INSTANCE = 0
    INSTANCE = 1
    UNKNOWN = 2


class Document:
    def __init__(self, raw_doc: str, is_instance: DocumentClass):
        self.raw_doc = raw_doc
        self.is_instance = is_instance
        self.__build_doc_vocabulary()

    def __build_doc_vocabulary(self):
        parser = BeautifulSoup(self.raw_doc, 'html.parser')

        clean_up_tags = ['scripts', 'style']

        # Remove tags from document
        for clean_up_tag in clean_up_tags:
            for tag in parser(clean_up_tag):
                tag.extract()

        # Remove ancor but keep content
        anchor_texts = []
        non_breaking_space = '\xa0'
        for anchor in parser('a'):
            anchor_text = anchor.string
            if anchor_text is not None and len(anchor_text) > 1 and anchor_text != non_breaking_space:
                anchor_texts.append(anchor_text)

        anchor_words = [tokenize(anchor_text) for anchor_text in anchor_texts]

        # Parse from matrix to list
        flatten_words = [item for sublist in anchor_words for item in sublist]

        doc_text = parser.get_text()
        doc_words = tokenize(doc_text) + flatten_words

        self.vocabulary = {}

        stemmer = nltk.stem.porter.PorterStemmer()
        for word in doc_words:
            token = stemmer.stem(word).lower()
            word_freq = self.vocabulary.get(token, 0)
            self.vocabulary[token] = word_freq + 1

    def get_feature_vector(self, features: List[str]) -> (List[int], DocumentClass):
        vector = [0]*len(features)
        for i, feature in enumerate(features):
            vector[i] = self.vocabulary.get(feature, 0)

        return vector, self.is_instance

    @staticmethod
    def load_from_url(url: str, is_instance: DocumentClass):
        req = requests.get(url)
        if req.status_code == 200:
            return Document(req.content.decode('utf-8'), is_instance)


if __name__ == '__main__':
    doc = Document.load_from_url('https://www.vivavinho.com.br/vinho-rose-italiano-wave-rosato-igt-750ml/p', DocumentClass.INSTANCE)
    print(doc.vocabulary)
