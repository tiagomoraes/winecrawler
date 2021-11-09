from abc import ABC, abstractmethod
from datetime import datetime as dt
from typing import List, Tuple

from sklearn.model_selection import StratifiedKFold
from sklearn.utils import shuffle
import numpy as np
from classification.helpers.utils import compute_metrics, doc_class_to_int, print_metrics

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from classification.feature_extractors import FeatureExtractor
    from classification.helpers.document import Document, DocumentClass


class Classifier(ABC):
    def __init__(self, feature_extractor: 'FeatureExtractor'):
        super().__init__()
        self.feature_extractor = feature_extractor

    @abstractmethod
    def train(self, docs: List['Document'], train_size: float, verbose: bool):
        pass

    @abstractmethod
    def predict(self, docs: List['Document']) -> List['DocumentClass']:
        pass

    @abstractmethod
    def predict_proba(self, docs: List['Document']) -> [float]:
        pass


class AccuracyWeightedEnsemble:
    def __init__(self, classifiers: List[Classifier]):
        clfs = []
        for clf in classifiers:
            clfs.append({
                'acc': 0,
                'clf': clf,
            })
        self.clfs = clfs
        self.trained = False

    def train(self, docs: List['Document'], train_size: float = 1.0, verbose: bool = False):
        start_time = dt.now()
        positive_docs = list(filter(lambda doc: doc.is_instance == 1, docs))
        negative_docs = list(filter(lambda doc: not doc.is_instance == 1, docs))

        total_positive = int(len(positive_docs) * train_size)
        total_negative = int(len(negative_docs) * train_size)

        train_docs = positive_docs[:total_positive] + negative_docs[:total_negative]
        train_docs = shuffle(train_docs)

        test_docs = positive_docs[total_positive:] + negative_docs[total_negative:]
        test_docs = shuffle(test_docs)

        docs = np.array(docs)
        labels = np.array(doc_class_to_int([doc.is_instance for doc in docs]))
        kfold = StratifiedKFold(n_splits=10)
        for clf in self.clfs:
            accs = []
            for train_index, test_index in kfold.split(docs, labels):
                clf['clf'].train(docs[train_index], train_size=train_size, verbose=verbose)
                preds = clf['clf'].predict(docs[test_index])
                y = labels[test_index]
                _, acc, _, _, _ = compute_metrics(preds, y)
                accs.append(acc)
            clf['acc'] = np.mean(accs)

        sum_acc = 0.0
        for clf in self.clfs:
            clf['clf'].train(train_docs, train_size=train_size, verbose=verbose)
            sum_acc += clf['acc']

        self.total_acc = sum_acc

        if len(test_docs) > 0:
            preds = self._internal_predict(test_docs)
            y = doc_class_to_int([doc.is_instance for doc in test_docs])

            if verbose:
                print_metrics(preds, y)

        if verbose:
            end_time = dt.now()
            train_duration = (end_time - start_time).total_seconds()
            print("Training took {} seconds".format(train_duration))

        self.trained = True

    def predict(self, docs: List['Document']) -> List[Tuple[int, 'DocumentClass']]:
        if not self.trained:
            raise AssertionError("Ensemble not trained yet. Call train before predict.")
        res = []
        for clf in self.clfs:
            probs = clf['clf'].predict_proba(docs)
            for i in range(len(probs)):
                probs[i][0] *= clf['acc']
                probs[i][1] *= clf['acc']
            res.append(probs)

        tp0 = [0.0] * len(docs)
        tp1 = [0.0] * len(docs)
        for i in range(len(docs)):
            for j in range(len(self.clfs)):
                tp0[i] += res[j][i][0]
                tp1[i] += res[j][i][1]

        tp0 = list(map(lambda v: (v / self.total_acc), tp0))
        tp1 = list(map(lambda v: (v / self.total_acc), tp1))

        out = []
        for i in range(len(docs)):
            label = 1 if tp1[i] > tp0[i] else 0
            out.append((i, label))

        return out

    # Bypass predict trained check for usage inside train method
    def _internal_predict(self, docs: List['Document']) -> List['DocumentClass']:
        temp = self.trained
        self.trained = True

        result = self.predict(docs)

        self.trained = temp
        return [doc[1] for doc in result]
