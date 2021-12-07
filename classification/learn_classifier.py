import os

from classification.feature_extractors import MostFrequentWordsExtractor, DocFrequencyDifferenceExtractor, \
    PlainFrequencyDifferenceExtractor, MixedFrequencyDifferenceExtractor
from classification.helpers.corpus_loader import load_documents, load_corpus
from classification.helpers.document import DocumentClass
from classification.helpers.utils import ClassifierType
from classification.generic_classifier import DocumentClassifier


def classify_crawler_samples(clf: DocumentClassifier, folder: str):
    overall_positive = 0
    overall_total = 0
    for site_root in os.listdir(folder):
        root_folder = os.path.join(folder, site_root)
        print(f' Calculating for {root_folder}')
        docs = load_documents(root_folder)
        results = clf.predict(docs)
        insts = [res[0] for res in results if res[1] == DocumentClass.INSTANCE]
        non_insts = [res[0] for res in results if res[1] == DocumentClass.NON_INSTANCE]
        overall_positive += len(insts)
        overall_total += (len(insts) + len(non_insts))
        print(len(insts), insts)
        print(f'positive / total = {len(insts)} / {(len(insts) + len(non_insts))} = {len(insts) / (len(insts) + len(non_insts))}')

    print(f'positive / total = {overall_positive} / {overall_total} = {overall_positive / overall_total}')


def main():
    inst_dir = os.path.join(cd, 'samples/samples_pages')
    non_inst_dir = os.path.join(cd, 'samples/nonsamples_pages')
    corpus = load_corpus(inst_dir, non_inst_dir).drop_stop_words()

    print('\nFrequent words:')
    for token in corpus.vocabulary:
        occurrences = corpus.vocabulary[token].get_all_docs()
        frequencies = corpus.vocabulary[token].get_total_freq()
        total_docs = len(corpus.documents)
        if total_docs * .4 < len(occurrences):
            print("{} = {}, {}, {}".format(token, occurrences, len(occurrences), frequencies))

    return
    most_frequent_words_selector = MostFrequentWordsExtractor(corpus)
    doc_frequency_diff_selector = DocFrequencyDifferenceExtractor(corpus)
    plain_frequency_diff_selector = PlainFrequencyDifferenceExtractor(corpus)
    mixed_frequency_diff_selector = MixedFrequencyDifferenceExtractor(corpus)

    # n_features = 50
    # print('')
    # print("MostFrequentWordsExtractor: {}".format(most_frequent_words_selector.get_feature_words(n_features)))
    # print()
    # print("DocFrequencyDifferenceExtractor: {}".format(doc_frequency_diff_selector.get_feature_words(n_features)))
    # print()
    # print("PlainFrequencyDifferenceExtractor: {}".format(plain_frequency_diff_selector.get_feature_words(n_features)))
    # print()
    # print("MixedFrequencyDifferenceExtractor: {}".format(mixed_frequency_diff_selector.get_feature_words(n_features)))
    # print()

    for i, s in enumerate([doc_frequency_diff_selector]):
        print('*************************')
        # selector_name = {0: 'Most Frequent Words', 1: 'Doc Frequency Diff', 2: 'Plain Frequency Diff', 3: 'Mixed Frequency Diff'}
        # print(f'\n{selector_name[i]}')
        print(f'\nDoc Frequency Diff')
        dc = DocumentClassifier(s)

        print('\nNAIVE_BAYES:')
        dc.train(corpus.documents, ClassifierType.NAIVE_BAYES, train_size=.7, verbose=False)
        classify_crawler_samples(dc, './../crawler/bfs_pages')

        print('\nDECISION_TREE:')
        dc.train(corpus.documents, ClassifierType.DECISION_TREE, train_size=.7, verbose=False)
        classify_crawler_samples(dc, './../crawler/bfs_pages')

        print('\nSVM:')
        dc.train(corpus.documents, ClassifierType.SVM, train_size=.7, verbose=False)
        classify_crawler_samples(dc, './../crawler/bfs_pages')

        print('\nLOGISTIC_REGRESSION:')
        dc.train(corpus.documents, ClassifierType.LOGISTIC_REGRESSION, train_size=.7, verbose=False)
        classify_crawler_samples(dc, './../crawler/bfs_pages')

        print('\nMULTILAYER_PERCEPTRON:')
        dc.train(corpus.documents, ClassifierType.MULTILAYER_PERCEPTRON, train_size=.7, verbose=False)
        classify_crawler_samples(dc, './../crawler/bfs_pages')


if __name__ == '__main__':
    cd = os.getcwd()
    main()
