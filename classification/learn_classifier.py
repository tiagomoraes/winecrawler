import os

from classification.classifier import AccuracyWeightedEnsemble
from classification.feature_extractors import MostFrequentWordsExtractor, DocFrequencyDifferenceExtractor, \
    PlainFrequencyDifferenceExtractor, MixedFrequencyDifferenceExtractor
from classification.helpers.corpus_loader import load_documents, load_corpus
from classification.helpers.document import DocumentClass
from classification.mlp import MLPDocumentClassifier


def classify_crawler_samples(clf: AccuracyWeightedEnsemble, folder: str):
    _dir = os.path.join(os.path.join(os.path.join(cd, 'src'), 'crawler'), folder)

    for site_root in os.listdir(_dir):
        root_folder = os.path.join(_dir, site_root)
        docs = load_documents(root_folder)
        print(root_folder + ':')
        results = clf.predict(docs)
        insts = [res for res in results if res == DocumentClass.INSTANCE]
        non_insts = [res for res in results if res == DocumentClass.NON_INSTANCE]
        print(len(insts))
        print(len(non_insts))


def main():
    inst_dir = os.path.join(cd, 'samples/samples_pages')
    non_inst_dir = os.path.join(cd, 'samples/nonsamples_pages')
    corpus = load_corpus(inst_dir, non_inst_dir).drop_stop_words(in_place=True)

    print('\nFrequent words:')
    for token in corpus.vocabulary:
        occurrences = len(corpus.vocabulary[token].get_all_docs())
        total_docs = len(corpus.documents)
        if total_docs * .4 < occurrences:
            print("{} = {}".format(token, occurrences))

    selector = MostFrequentWordsExtractor(corpus)
    selector2 = DocFrequencyDifferenceExtractor(corpus)
    selector3 = PlainFrequencyDifferenceExtractor(corpus)
    selector4 = MixedFrequencyDifferenceExtractor(corpus)

    n_features = 50
    feature_words = selector.get_feature_words(n_features)
    feature_words2 = selector2.get_feature_words(n_features)
    feature_words3 = selector3.get_feature_words(n_features)
    feature_words4 = selector4.get_feature_words(n_features)

    print('')
    print("MostFrequentWordsExtractor: {}".format(feature_words))
    print()
    print("DocFrequencyDifferenceExtractor: {}".format(feature_words2))
    print()
    print("PlainFrequencyDifferenceExtractor: {}".format(feature_words3))
    print()
    print("MixedFrequencyDifferenceExtractor: {}".format(feature_words4))
    print()

    mlp = MLPDocumentClassifier(selector)
    mlp2 = MLPDocumentClassifier(selector2)
    mlp3 = MLPDocumentClassifier(selector3)
    mlp4 = MLPDocumentClassifier(selector4)

    ensemble = AccuracyWeightedEnsemble([mlp2])
    ensemble.train(corpus.documents, train_size=.7, verbose=True)

    classify_crawler_samples(ensemble, 'pages')


if __name__ == '__main__':
    cd = os.getcwd()
    main()
