
import numpy as np

import utils.classification_exceptions as e

# abstract class
class StackedGeneralization:
    def __init__(self, intermediate_classifiers={}):
        self.classifiers = intermediate_classifiers
        self.classlabels = []

    def register_classifiers(self):
        self.classifier2idx = {}
        self.idx2classifier = {}
        for idx, key in enumerate(self.classifiers.keys()):
            self.classifier2idx[key] = idx
            self.idx2classifier[idx] = key

    def add_classifier(self, name, classifier):
        self.classifiers[name] = classifier
        self.register_classifiers()

    def delete_classifier(self, name):
        del self.classifiers[name]
        self.register_classifiers()

    def translate_shorttext_intfeatures(self, shorttext):
        feature_vec = np.zeros(len(self.classifier2idx))
        for key in self.classifier2idx:
            feature_vec[self.classifier2idx[key]] = self.classifiers[key].score(shorttext)
        return feature_vec

    def convert_traindata_vectors(self, classdict):
        self.classlabels = list(classdict.keys())
        self.labels2idx = {}
        for idx, classlabel in enumerate(self.classlabels):
            self.labels2idx[classlabel] = idx

        X = []
        y = []
        for label in classdict:
            topicvecs = map(self.translate_shorttext_intfeatures, classdict[label])
            X += topicvecs
            y += [self.labels2idx[label]]*len(topicvecs)

        return X, y

    def train(self, classdict):
        raise e.NotImplementedException()

    def score(self, shorttext):
        raise e.NotImplementedException()

class LogisticStackedGeneralization(StackedGeneralization):
    pass