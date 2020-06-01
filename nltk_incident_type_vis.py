from typing import List

import matplotlib
import nltk
import pandas as pd

from report_data import ReportData
from report_data_d import ColName

report_df = ReportData(out_file_path="preprocess/data/data-processed.csv").get_processed_data()
descriptions = report_df[ColName.DESC]
it1: pd.Series = report_df[ColName.INC_T1]
it2: pd.Series = report_df[ColName.INC_T2]
c1 = it1.replace(to_replace='', value='UNKNOWN')
c2 = it2.replace(to_replace='', value='UNKNOWN')
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
