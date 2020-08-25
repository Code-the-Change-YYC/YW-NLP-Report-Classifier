import pickle
from typing import NewType

import en_core_web_lg
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.pipeline import Pipeline

from training.description_classification import model_paths

_nlp = None


def get_spacy_nlp():
    """Handles lazy loading of the Spacy NLP model.

    :return: The loaded Spacy model.
    """
    global _nlp
    if _nlp is None:
        _nlp = en_core_web_lg.load()
    return _nlp


def spacy_tokenizer(df_sent):
    nlp = get_spacy_nlp()
    spy_txt = nlp(df_sent)
    return [
        w.lemma_ if w.lemma_ != "-PRON-" else w.text
        for w in spy_txt
        if not w.is_stop and not w.is_punct
    ]


def nltk_tokenizer(df_sent):
    lemmatizer = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    tokens = word_tokenize(df_sent)
    words = [word.lower() for word in tokens if word.isalpha()]
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]

    return words


CNBPipeline = NewType('CNBPipeline', Pipeline)
"""Same as `sklearn.naive_bayes.ComplementNB` but accepts strings as inputs."""


def load_cnb() -> CNBPipeline:
    """Unpickles the trained ComplementNB description classifier, ensuring its
    dependencies are met.

    :return: The CNB classifier.
    """
    with open(model_paths.cnb, 'rb') as f:
        return pickle.load(f)


SVMPipeline = NewType('SVMPipeline', Pipeline)
"""Same as `sklearn.svm.SVC` but accepts strings as inputs."""


def load_svm() -> SVMPipeline:
    """Unpickles the trained SVM-C description classifier, ensuring its
    dependencies are met.

    :return: The SVM-C classifier.
    """
    with open(model_paths.svm, 'rb') as f:
        return pickle.load(f)
