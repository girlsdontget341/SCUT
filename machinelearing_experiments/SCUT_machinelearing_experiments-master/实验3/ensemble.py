import pickle
import numpy as np
from sklearn.tree import DecisionTreeClassifier


class AdaBoostClassifier:
    '''A simple AdaBoost Classifier.'''

    def __init__(self, weak_classifier, n_weakers_limit):
        '''Initialize AdaBoostClassifier

        Args:
            weak_classifier: The class of weak classifier, which is recommend to be sklearn.tree.DecisionTreeClassifier.
            n_weakers_limit: The maximum number of weak classifier the model can use.
        '''
        self.weak_classifier_list = []
        self.classifier_weight = []
        self.n_weakers_limit = n_weakers_limit
        self.Hx = []
        self.pred_list = []

    def fit(self, X, y):
        '''Build a boosted classifier from the training set (X, y).
        Args:
            X: An ndarray indicating the samples to be trained, which shape should be (n_samples,n_features).
            y: An ndarray indicating the ground-truth labels correspond to X, which shape should be (n_samples,1).
        '''

        self.Hx = np.zeros((len(y), self.n_weakers_limit))
        weight = np.full(shape=(X.shape[0]), fill_value=1/X.shape[0])
        print(weight.shape)
        for iters in range(self.n_weakers_limit):

            weak_classifier = DecisionTreeClassifier(
            criterion='entropy',
            splitter='random',
            max_features='log2',
            max_depth=10,
            max_leaf_nodes=10,
            min_samples_split=10,
            min_samples_leaf=3,
            class_weight='balanced'
            )

            weak_classifier.fit(X, y, sample_weight=weight)
            hx = weak_classifier.predict(X)
            score = weak_classifier.score(X, y)

            print('score {}: '.format(iters+1), score)

            error = 1 - score
            alpha = 0.5 * np.log((1-error)/error)

            exp = np.exp(-alpha * np.multiply(hx, y.flatten()))
            exp = np.array(exp).flatten()
            weight = np.multiply(weight, exp)
            zm = np.sum(weight)
            weight = weight / zm

            if(score>0.5):
                self.classifier_weight.append(alpha)
                self.weak_classifier_list.append(weak_classifier)
                self.Hx[:,iters] = alpha*np.array(hx)
                self.pred_list.append(np.array(hx))

    def predict_scores(self, X, y):
        '''Calculate the weighted sum score of the whole base classifiers for given samples.

        Args:
            X: An ndarray indicating the samples to be predicted, which shape should be (n_samples,n_features).

        Returns:
            An one-dimension ndarray indicating the scores of differnt samples, which shape should be (n_samples,1).
        '''
        Hx = np.zeros((len(y), self.n_weakers_limit))
        for i in range(len(self.weak_classifier_list)):
            hx = self.weak_classifier_list[i].predict(X)
            Hx[:,i] = self.classifier_weight[i]*np.array(hx)
        pred = np.sum(Hx, axis=1)
        pred = (pred>=1)
        accuracy = (pred==y.flatten())
        return np.mean(accuracy)

    def predict(self, X, threshold=0):
        '''Predict the catagories for given samples.

        Args:
            X: An ndarray indicating the samples to be predicted, which shape should be (n_samples,n_features).
            threshold: The demarcation number of deviding the samples into two parts.

        Returns:
            An ndarray consists of predicted labels, which shape should be (n_samples,1).
        '''
        Hx = np.zeros((X.shape[0], self.n_weakers_limit))
        for i in range(len(self.weak_classifier_list)):
            hx = self.weak_classifier_list[i].predict(X)
            Hx[:,i] = self.classifier_weight[i]*np.array(hx)
        pred = np.sum(Hx, axis=1)
        pred[pred>=1] = 1
        pred[pred<1] = 0
        return pred

    @staticmethod
    def save(model, filename):
        with open(filename, "wb") as f:
            pickle.dump(model, f)

    @staticmethod
    def load(filename):
        with open(filename, "rb") as f:
            return pickle.load(f)


