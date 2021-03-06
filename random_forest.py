from collections import Counter
import numpy as np
import pandas as pd

from decision_tree import DecisionTree

def bootstrap_sample(X, y):
    n_samples = X.shape[0]
    idxs = np.random.choice(n_samples, size=n_samples, replace=True)
    return X[idxs], y[idxs]


def most_common_label(y):
    counter = Counter(y)
    most_common = counter.most_common(1)[0][0]
    return most_common


class RandomForest:
    def __init__(self, n_trees=100, min_samples_split=2, max_depth=100, n_feats=None):
        self.n_trees = n_trees
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth
        self.n_feats = n_feats
        self.trees = []

    def fit(self, X, y):
        self.trees = []
        for _ in range(self.n_trees):
            tree = DecisionTree(
                min_samples_split=self.min_samples_split,
                max_depth=self.max_depth,
                n_feats=self.n_feats,
            )
            X_samp, y_samp = bootstrap_sample(X, y)
            tree.fit(X_samp, y_samp)
            self.trees.append(tree)

    def predict(self, X):
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        #[1111 0000 1111]
        tree_preds = np.swapaxes(tree_preds, 0, 1)
        #[101 101 101 101]
        y_pred = [most_common_label(tree_pred) for tree_pred in tree_preds]
        return np.array(y_pred)


# Testing
if __name__ == "__main__":

    from sklearn.model_selection import train_test_split

    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    df = pd.read_csv("dataset.csv", delimiter=",")
    df.info()
    data = df.to_numpy()
    print(data.shape)
    n_samples, n_features = data.shape
    n_features -= 1
    X = data[:,0:n_features]
    y = data[:, n_features]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=100)
    clf = RandomForest(n_trees=50, max_depth=10)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

    acc = accuracy(y_test, y_pred)
    print("Accuracy:", acc)