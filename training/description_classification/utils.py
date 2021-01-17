import pickle
from typing import NewType, Iterable

import en_core_web_lg
import matplotlib.pyplot as plt
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score, balanced_accuracy_score, classification_report, plot_confusion_matrix
from sklearn.pipeline import Pipeline

from preprocess.incident_types.incident_types_d import IncidentType
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


def load_cnb(model_path: str, copy_from_prod: bool = True) -> CNBPipeline:
    """Unpickles the trained ComplementNB description classifier, ensuring its
    dependencies are met.

    Params:
        model_path: The path to the pickled model. If this is not the production
        model, a copy of the production model is made at `model_path`, unless
        `copy_from_prod` is `False`, in which case `model_path` is attempted to
        be loaded.

    Returns: The CNB classifier.
    """
    if model_path != model_paths.cnb and copy_from_prod:
        with open(model_paths.cnb, 'rb') as prod_model, open(model_path, 'wb') as model:
            model_contents = prod_model.read()
            model.write(model_contents)
            return pickle.loads(model_contents)
    else:
        with open(model_path, 'rb') as model_file:
            return pickle.load(model_file)            
    

def save_cnb(model: CNBPipeline, model_path: str):
    """Save the CNB model.
    
    Params:
        model: The model to save.
        model_path: The path of the file to save the model to.
    """
    with open(model_path, 'wb') as model_file:
        pickle.dump(model, model_file)



SVMPipeline = NewType('SVMPipeline', Pipeline)
"""Same as `sklearn.svm.SVC` but accepts strings as inputs."""


def load_svm() -> SVMPipeline:
    """Unpickles the trained SVM-C description classifier, ensuring its
    dependencies are met.

    :return: The SVM-C classifier.
    """
    with open(model_paths.svm, 'rb') as f:
        return pickle.load(f)


def count_weight(labels: Iterable):
    """Assigns each label class a weight according to it's frequency of appearance in the dataset.

    :param labels:
    :return: Dictionary with labels as keys and count weights as values.
    """
    weight_dict = {lb: 0 for lb in set(labels)}

    for label in labels:
        weight_dict[label] += 1

    return weight_dict


def show_classification_report(clf: Pipeline, X, y, sample_weight=None):
    predicted = clf.predict(X)
    accuracy = accuracy_score(y, predicted, sample_weight=sample_weight)
    balanced = balanced_accuracy_score(
        y, predicted, sample_weight=sample_weight
    )

    print("Accuracy: {:.2%}".format(accuracy))
    print("Balanced accuracy: {:.2%}".format(balanced))
    print()

    labels = [e.value for e in IncidentType]
    print("Classification report:\n")
    print(
        classification_report(
            y,
            predicted,
            sample_weight=sample_weight,
            labels=labels,
            target_names=labels,
            zero_division=0
        )
    )
    
    true = set(y)
    pred = set(predicted)
    display = plot_confusion_matrix(
        clf,
        X,
        y,
        sample_weight=sample_weight,
        normalize="true",
        display_labels=true | pred,
        cmap=plt.cm.Blues,
        xticks_rotation="vertical",
    )
    title = "Confusion matrix with normalization"
    display.ax_.set_title(title)
