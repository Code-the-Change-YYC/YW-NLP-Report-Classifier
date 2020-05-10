from typing import List

import matplotlib
import nltk
import pandas as pd

from scrubber.data import columns

report_data = pd.read_csv("data-sensitive.csv", na_filter=False)
report_data.columns = columns
descriptions = report_data["DESCRIPTION"]
it1: pd.Series = report_data["INCIDENT_TYPE_1"]
it1o: pd.Series = report_data["INCIDENT_1_OLD"]
it2: pd.Series = report_data["INCIDENT_TYPE_2"]
it2o: pd.Series = report_data["INCIDENT_TYPE_OTHER"]
c1: pd.Series = it1 + it1o
c2: pd.Series = it2 + it2o
c1 = c1.replace(to_replace='', value='UNKNOWN')
c2 = c2.replace(to_replace='', value='UNKNOWN')
stopwords: List = [*nltk.corpus.stopwords.words('english'), '.', ',']
tokenized = [nltk.tokenize.word_tokenize(description) for description in descriptions]
descriptions = [[word.lower() for word in description if word not in stopwords]
                for description in tokenized]


def flatten(_list: List[List]) -> List:
    return [item for sub_list in _list for item in sub_list]


fd = nltk.FreqDist(flatten(descriptions))
most_common = [c[0] for c in fd.most_common(10)]
pairs = flatten([[(pair[0], word) for word in pair[1] if word in most_common]
                 for pair in zip(c1, descriptions)])
cfd = nltk.ConditionalFreqDist(pairs)
matplotlib.rc('figure', figsize=[30, 20])
cfd.plot()
