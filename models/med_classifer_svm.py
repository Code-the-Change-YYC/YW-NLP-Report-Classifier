"""
This classification model is designed to use nltk and sci-kit learn python library in order to
train and predict whether the customer descriptions can indicate the whether this incident is medical
emergency or it is not medical emergency

"""
import collections
import string

#NLTK libarary
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.stem.snowball import SnowballStemmer


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#sci-kit learn imports
from sklearn.svm import LinearSVC
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
# we should also explore on Tfidfvector as well
#https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html
import re

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

# NLTK tokenizer for text clean and lemmatization
def nltk_tokenizer(df_sent):
    lemmatizer = nltk.WordNetLemmatizer()
    stop_words = set(stopwords.words("english"))

    tokens = word_tokenize(df_sent)
    words = [word.lower() for word in tokens if word.isalpha() ]  # get rid of puntuation
    words = [word for word in words if word not in stop_words]
    words = [lemmatizer.lemmatize(word) for word in words]

    return words

# Basic file read and large model for spacy
file_name = "data-processed.csv"

yw_df = pd.read_csv(file_name)


# actual loading data + modeling

yw_clean = clean_personinfo(yw_df["DESCRIPTION"])

# basic encoding for binary classification. If we consider oneVsAll model, we can consider explore the encoders in sci-kit learn
yw_txt_cats = ywca_pd_types = [1 if t == 'Medical emergency' else 0 for t in yw_df["INCIDENT_TYPE_1"]]


# vector here I test with basic count vector. we can consider TF-IDF vector in ski-learn as possible better performance.
# parameter fine tuning: I set basic way we can play here. you can set to empty and see the difference to play around.
# vectorizer = CountVectorizer(tokenizer=nltk_tokenizer,ngram_range=(1,2),lowercase=True,min_df = 2)
# yw_clean= vectorizer.fit_transform(yw_clean)


#basic split
X_train_set, X_test_set, y_train_set, y_test_set = train_test_split(
    yw_clean, yw_txt_cats, train_size=0.8, random_state=1, shuffle=True)


svc = LinearSVC()


#better way to organize the final pipeline built in sklearn

text_pipe = make_pipeline(CountVectorizer(tokenizer=nltk_tokenizer, token_pattern=r'\b\w+\b', ngram_range=(1, 2),
                           min_df=2),
                          TfidfTransformer(),  ## optional
                          LinearSVC())


#pipe train and score
text_pipe.fit(X_train_set, y_train_set)
#To show pipe score without parameter tune
print("text pipeline score on test data {:.2%}".format(text_pipe.score(X_test_set,y_test_set)))

#cv grid is designed for deeper model hyperparameter fine tuning

#example go with linear svc specific.
# grid parameter setting is in dictionary form. for name and convention please review the documentation on CVgrid, this part
# was my original plan to read into more and try to increase and test every hyperparameter fine tunes to see what best matches.
param_grid = {'linearsvc__C':np.logspace(-5,0,6)}
grid = GridSearchCV(text_pipe,param_grid,cv = 5)
grid.fit(X_train_set,y_train_set)

#show you best score and hyperparameter.
print("grid best score cross validation at {:.2%}".format(grid.best_score_))
print("best grid parameters are :{}".format(grid.best_params_))

