import os

from classification.classifier import AccuracyWeightedEnsemble
from classification.feature_extractors import MostFrequentWordsExtractor, DocFrequencyDifferenceExtractor, \
    PlainFrequencyDifferenceExtractor, MixedFrequencyDifferenceExtractor
from classification.helpers.corpus_loader import load_documents, load_corpus
from classification.helpers.document import DocumentClass
from classification.helpers.utils import ClassifierType
from classification.mlp import DocumentClassifier


def classify_crawler_samples(clf: DocumentClassifier, folder: str):
    _dir = os.path.join(os.path.join(cd, 'samples'), folder)

    for site_root in os.listdir(_dir):
        root_folder = os.path.join(_dir, site_root)
        docs = load_documents(root_folder)
        print(root_folder + ':')
        results = clf.predict(docs)
        insts = [res for res in results if res[1] == DocumentClass.INSTANCE]
        non_insts = [res for res in results if res[1] == DocumentClass.NON_INSTANCE]
        print(len(insts), insts)
        print(len(non_insts), non_insts)


def main():
    inst_dir = os.path.join(cd, 'samples/samples_pages')
    non_inst_dir = os.path.join(cd, 'samples/nonsamples_pages')
    corpus = load_corpus(inst_dir, non_inst_dir).drop_stop_words(in_place=True)

    # print('\nFrequent words:')
    # for token in corpus.vocabulary:
    #     occurrences = corpus.vocabulary[token].get_all_docs()
    #     frequencies = corpus.vocabulary[token].get_total_freq()
    #     total_docs = len(corpus.documents)
    #     if total_docs * .4 < len(occurrences):
    #         print("{} = {}, {}".format(token, occurrences, frequencies))

    selector = MostFrequentWordsExtractor(corpus)
    selector2 = DocFrequencyDifferenceExtractor(corpus)
    selector3 = PlainFrequencyDifferenceExtractor(corpus)
    selector4 = MixedFrequencyDifferenceExtractor(corpus)

    # n_features = 50
    # feature_words = selector.get_feature_words(n_features)
    # feature_words2 = selector2.get_feature_words(n_features)
    # feature_words3 = selector3.get_feature_words(n_features)
    # feature_words4 = selector4.get_feature_words(n_features)
    #
    # print('\nFrequent words:')
    # for token in feature_words2:
    #     occurrences = corpus.vocabulary[token].get_all_docs()
    #     frequencies = corpus.vocabulary[token].get_total_freq()
    #     total_docs = len(corpus.documents)
    #     if total_docs * .4 < len(occurrences):
    #         print("{} = {}, {}".format(token, occurrences, frequencies))

    # print('')
    # print("MostFrequentWordsExtractor: {}".format(feature_words))
    # print()
    # print("DocFrequencyDifferenceExtractor: {}".format(feature_words2))
    # print()
    # print("PlainFrequencyDifferenceExtractor: {}".format(feature_words3))
    # print()
    # print("MixedFrequencyDifferenceExtractor: {}".format(feature_words4))
    # print()

    # mlp = DocumentClassifier(selector)
    # mlp2 = DocumentClassifier(selector2)
    # mlp3 = DocumentClassifier(selector3)
    # mlp4 = DocumentClassifier(selector4)

    # ensemble = AccuracyWeightedEnsemble([mlp2])
    # ensemble.train(corpus.documents, train_size=.7, verbose=True)

    # selector = MostFrequentWordsExtractor(corpus)
    # selector2 = DocFrequencyDifferenceExtractor(corpus)
    # selector3 = PlainFrequencyDifferenceExtractor(corpus)
    # selector4 = MixedFrequencyDifferenceExtractor(corpus)

    for i, s in enumerate([selector, selector2, selector3, selector4]):
        print('*************************')
        selector_name = {0: 'Most Frequent Words', 1: 'Doc Frequency Diff', 2: 'Plain Frequency Diff', 3: 'Mixed Frequency Diff'}
        print(f'\n{selector_name[i]}')
        dc = DocumentClassifier(s)

        print('\nNAIVE_BAYES:')
        dc.train(corpus.documents, ClassifierType.NAIVE_BAYES, train_size=.7, verbose=True)
        classify_crawler_samples(dc, 'pages')

        print('\nDECISION_TREE:')
        dc.train(corpus.documents, ClassifierType.DECISION_TREE, train_size=.7, verbose=True)
        classify_crawler_samples(dc, 'pages')

        print('\nSVM:')
        dc.train(corpus.documents, ClassifierType.SVM, train_size=.7, verbose=True)
        classify_crawler_samples(dc, 'pages')

        print('\nLOGISTIC_REGRESSION:')
        dc.train(corpus.documents, ClassifierType.LOGISTIC_REGRESSION, train_size=.7, verbose=True)
        classify_crawler_samples(dc, 'pages')

        print('\nMULTILAYER_PERCEPTRON:')
        dc.train(corpus.documents, ClassifierType.MULTILAYER_PERCEPTRON, train_size=.7, verbose=True)
        classify_crawler_samples(dc, 'pages')


if __name__ == '__main__':
    cd = os.getcwd()
    main()
