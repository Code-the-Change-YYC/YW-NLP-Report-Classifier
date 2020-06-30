"""
This classification model is designed to use Spacy and sci-kit learn python library in order to
train and predict whether the customer descriptions can indicate the whether this incident is medical
emergency or it is not medical emergency

"""
import collections
import string

# NLTK libarary
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
# we can explore on stemmer too
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# sci-kit learn imports
from sklearn.linear_model import LogisticRegression, SGDClassifier

from sklearn.naive_bayes import MultinomialNB, BernoulliNB

from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV

# explained variance score can also be good measure alternative to default jaccard score (coefficient )
# jaccard score:"defined as the size of the intersection divided by the size of the union of two label sets,
# is used to compare set of predicted labels for a sample to the corresponding set of labels in y_true."

# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.jaccard_score.html?highlight=jaccard_score#sklearn.metrics.jaccard_score
# https://scikit-learn.org/stable/modules/generated/sklearn.metrics.accuracy_score.html

# option we can consider explore
from sklearn.metrics import explained_variance_score
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# we should also explore on Tfidfvector as well
# https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
import spacy, re
from spacy.lang.en.stop_words import STOP_WORDS

# Basic file read and large model for spacy
file_name = "data-processed.csv"
# uncomment when you need to test Spacy.io and make sure download the model to local before run.
# nlp = spacy.load("en_core_web_lg")
yw_df = pd.read_csv(file_name)


# simple ways of clean and hide entities
def clean_personinfo(df):
    """

    :param df:
    :type df:
    :return:
    :rtype:
    """
    replace_word = "someone"
    return [re.sub(r"\{\{[^\{\}]+\}\}\w?", replace_word, str1) for str1 in df]


# basic spacy text clean and lemmatization
def spacy_tokenizer(df_sent):
    """

    :param df:
    :type df:
    :return:
    :rtype:
    """
    spy_txt = nlp(df_sent)
    return [w.lemma_ if w.lemma_ != "-PRON-" else w.text
            for w in spy_txt
            if w.is_stop == False
            and not w.is_punct
            and not w.is_space
            and not w.pos_ == "PRON"]


# NLTK tokenizer for text clean and lemmatization
def nltk_tokenizer(df_sent):
    lemmatizer = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    tokens = word_tokenize(df_sent)
    words = [word.lower() for word in tokens if word.isalpha()]  # get rid of puntuation
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]

    return words


# this method was designed to find tokens, which are not punctuation or letters, are considered to be "bad tokens" for me,
# They are either entities, numbers, time stamp or address stree number.

def nltk_checkup_tokenizer(df_sent):
    df_sent = df_sent.translate(str.maketrans('', '', string.punctuation))
    tokens = word_tokenize(df_sent)
    words = [word for word in tokens if not word.isalpha()]  # get rid of puntuation
    return words


# This function basically display a bar diagram shows in blue is postive classfied and red is negative classfied
def visualize_coefficients(classifier, feature_names, n_top_features=25):
    # get coefficients with large absolute values
    coef = classifier.coef_.ravel()
    positive_coefficients = np.argsort(coef)[-n_top_features:]
    negative_coefficients = np.argsort(coef)[:n_top_features]
    interesting_coefficients = np.hstack([negative_coefficients, positive_coefficients])
    # plot them
    plt.figure(figsize=(10, 10), tight_layout=True)
    colors = ["red" if c < 0 else "blue" for c in coef[interesting_coefficients]]
    plt.bar(np.arange(2 * n_top_features), coef[interesting_coefficients], color=colors)
    feature_names = np.array(feature_names)
    plt.xticks(np.arange(1, 1 + 2 * n_top_features), feature_names[interesting_coefficients], rotation=60, ha="right");
    plt.show()


# actual loading data + modeling

yw_clean = clean_personinfo(yw_df["DESCRIPTION"])

# if we need to look at bad tokens uncomment below:

# ******print total token length and compare to the bad tokens amount

# total_token  =  []
# for sent in yw_clean:
#     for w in word_tokenize(sent):
#         total_token.append(w)
#
# print(len(set(total_token)))
# final_bad_tokens =[]
# for sent in yw_clean:
#     list = nltk_checkup_tokenizer(sent)
#     if list != []:
#             for item in list:
#                 final_bad_tokens.append(item)
# print(len(set(final_bad_tokens)))


# basic encoding for binary classification. If we consider oneVsAll model, we can consider explore the encoders in sci-kit learn
yw_txt_cats = ywca_pd_types = [1 if t == 'Medical emergency' else 0 for t in yw_df["INCIDENT_TYPE_1"]]

# vector here I test with basic count vector. we can consider TF-IDF vector in ski-learn as possible better performance.
# parameter fine tuning: I set basic way we can play here. you can set to empty and see the difference to play around.
vectorizer = CountVectorizer(tokenizer=nltk_tokenizer, ngram_range=(1, 2), lowercase=True, min_df=2)
yw_clean = vectorizer.fit_transform(yw_clean)

# basic split
X_train_set, X_test_set, y_train_set, y_test_set = train_test_split(
    yw_clean, yw_txt_cats, train_size=0.8, random_state=1, shuffle=True)

# model list :

# linear model family
lr = LogisticRegression()
sgdc = SGDClassifier()

# naive bayes model family
multi = MultinomialNB()
bern = BernoulliNB()

models = [lr, sgdc, multi, bern]
models_name = ["logistic regression", "SGDC classifer", "multinominal", "bernoulli"]

for i, model in enumerate(models):
    train_t = model.fit(X_train_set, y_train_set)
    # score for test set
    score_train = model.score(X_test_set, y_test_set)
    # cross validate score
    cv_score = cross_val_score(model, X_train_set, y_train_set, cv=5)
    print(f"model {models_name[i]}, accuracy score is {score_train}.")
    print(f"model {models_name[i]}, CV score is {cv_score}.")  # not average here but we can produce a mean
    # this cross validate is based on k-fold k=5 here.
    # more hyperparameter reading below:
    # https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html?highlight=cross_val_score#sklearn.model_selection.cross_val_score

    # print out to answer Gary's question on how many misses we have in how many test cases.
    predicts = model.predict(X_test_set)
    y_labels = y_test_set
    different = []

    for i, predict in enumerate(predicts):
        if predict != y_labels[i]:
            different.append((predict, y_labels[i]))
    print(f"error count : {len(different)} , total was {len(predicts)}")

# #visual correlations: this is only apply for linear models. I have not figure a way to show in naive bays coeficient
# but I am sure there is a way in seaborn library for data visualization.
# https://seaborn.pydata.org/

visualize_coefficients(lr, vectorizer.get_feature_names())

# Here is an idea on tokenzier comparsion if we want to dig deep on different between spacy and nltk tokenizer
# spacy_tokens=[spacy_tokenizer(sent) for sent in yw_clean]
# nltk_tokens = [nltk_tokenizer(sent)for sent in yw_clean]

# diff_tokens=[]
#
# for index in range(len(spacy_tokens)):
#     if spacy_tokens[index] != nltk_tokens[index]:
#         diff_tokens.append((spacy_tokens[index],nltk_tokens[index]))
#         print(f"Spacy token is : {spacy_tokens[index]}")
#         print(f"NLTK token is : {nltk_tokens[index]}")
# print(len(diff_tokens))
