import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import ComplementNB
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC

from models.model import Model, ArrayLike
from models.utils import _clean_scrubadub_entities, nltk_tokenizer
from report_data import ReportData
from report_data_d import ColName


class CNBModel(Model):
    """Complement Naive Bayes model for classification."""

    def train(self, X: ArrayLike, y: ArrayLike) -> object:
        pass

    def predict(self, X: ArrayLike) -> np.ndarray:
        pass

    def partial_fit(self, X: ArrayLike, y: ArrayLike, classes: ArrayLike = None) -> object:
        pass


if __name__ == '__main__':
    cnb_model = CNBModel()
    report_data = ReportData()
    data = report_data.get_processed_data()
    data[ColName.DESC] = _clean_scrubadub_entities(data[ColName.DESC])
    # X = CountVectorizer(tokenizer=nltk_tokenizer, token_pattern=r'\b\w+\b', ngram_range=(1, 2),
    #                     min_df=2).fit_transform(data[ColName.DESC])
    X = TfidfVectorizer(tokenizer=nltk_tokenizer, token_pattern=r'\b\w+\b', ngram_range=(1, 2),
                        min_df=2).fit_transform(data[ColName.DESC])
    label_encoder = LabelEncoder()
    y = label_encoder.fit_transform(data[ColName.INC_T1])
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.9)
    complement_nb: ComplementNB = ComplementNB()
    svm_classifier: SVC = SVC()
    complement_nb.fit(X_train, y_train)
    svm_classifier.fit(X_train, y_train)
    nb_score = complement_nb.score(X_test, y_test)
    svm_score = svm_classifier.score(X_test, y_test)
    print(nb_score, svm_score)
