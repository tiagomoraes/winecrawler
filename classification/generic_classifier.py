from datetime import datetime as dt
from typing import Tuple, List

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.utils import shuffle

from classification.classifier import Classifier
from classification.feature_extractors import FeatureExtractor
from classification.helpers.document import Document, DocumentClass
from classification.helpers.utils import get_vectors_scaler, doc_class_to_int, print_metrics, get_vectors, \
    int_to_doc_class_with_doc_index, ClassifierType


class DocumentClassifier(Classifier):
    def __init__(self, feature_extractor: FeatureExtractor):
        super().__init__(feature_extractor)
        self.trained = False

    def train(self, docs: [Document], classifier_type: ClassifierType, train_size: float = 1.0, verbose: bool = False):
        start_time = dt.now()

        positive_docs = list(filter(lambda doc: doc.is_instance == DocumentClass.INSTANCE, docs))
        negative_docs = list(filter(lambda doc: not doc.is_instance == DocumentClass.INSTANCE, docs))

        total_positive = int(len(positive_docs)*train_size)
        total_negative = int(len(negative_docs)*train_size)

        train_docs = positive_docs[:total_positive] + negative_docs[:total_negative]
        train_docs = shuffle(train_docs)

        test_docs = positive_docs[total_positive:] + negative_docs[total_negative:]
        test_docs = shuffle(test_docs)

        self.features = self.feature_extractor.get_feature_words(num_features=50)

        classifiers = {
            classifier_type.NAIVE_BAYES: GaussianNB(),
            classifier_type.DECISION_TREE: DecisionTreeClassifier(),
            classifier_type.SVM: SVC(),
            classifier_type.LOGISTIC_REGRESSION: LogisticRegression(),
            classifier_type.MULTILAYER_PERCEPTRON: MLPClassifier()
        }
        clf = classifiers[classifier_type]
        # parameters = {'solver': ('adam', 'lbfgs', 'sgd'), 'activation': ('relu', 'identity', 'tanh', 'logistic'), 'learning_rate_init': (0.001, 0.005, 0.01)}
        # clf = GridSearchCV(clf, parameters, scoring='accuracy', verbose=1)

        self.clf = clf

        x, y, self.scaler = get_vectors_scaler(self.features, train_docs)

        self.clf.fit(x, y)

        if len(test_docs) > 0:
            final_preds = self._internal_predict(test_docs)
            final_preds = doc_class_to_int(final_preds)
            correct_preds = doc_class_to_int([test_doc.is_instance for test_doc in test_docs])

            if verbose:
                print_metrics(final_preds, correct_preds)

        if verbose:
            end_time = dt.now()
            train_duration = (end_time-start_time).total_seconds()
            print("Training took {} seconds".format(train_duration))
        self.trained = True

    def predict(self, docs: [Document]) -> List[Tuple[int, 'DocumentClass']]:
        if not self.trained:
            raise AssertionError("MLP not trained yet. Call train before predict.")

        x, _ = get_vectors(self.features, docs, self.scaler)
        preds = self.clf.predict(x)
        return [(i, pred) for i, pred in enumerate(preds)]

    def predict_proba(self, docs: List[Document]) -> [float]:
        if not self.trained:
            raise AssertionError("MLP not trained yet. Call train before predict.")

        x, _ = get_vectors(self.features, docs, self.scaler)
        preds = self.clf.predict_proba(x)
        return preds

    # Bypass predict trained check for usage inside train method
    def _internal_predict(self, docs: List[Document]) -> List[DocumentClass]:
        temp = self.trained
        self.trained = True

        result = self.predict(docs)

        self.trained = temp
        return [doc[1] for doc in result]
