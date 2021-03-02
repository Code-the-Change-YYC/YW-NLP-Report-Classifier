from preprocess.preprocessor import Preprocessor

import pandas as pd
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
next(wordnet.all_synsets()) # yapf: disable NOTE: ensures thread safety for lazyloading of wordnet
from preprocess.report_data_d import _ColName


class NLTKLemmatizer(Preprocessor):
    lemmatizer = WordNetLemmatizer()

    @staticmethod
    def nltk_to_wordnet(nltk_tag):
        """
        Params:
            nltk_tag: the nltk_tag object originating from the pos_tag() function from nltk.

        Returns:
            the wordnet tag object, e.g., wordnet.NOUN
        """

        if nltk_tag.startswith("J"):
            return wordnet.ADJ
        elif nltk_tag.startswith("V"):
            return wordnet.VERB
        elif nltk_tag.startswith("N"):
            return wordnet.NOUN
        elif nltk_tag.startswith("R"):
            return wordnet.ADV
        else:
            return None

    def process(self, report_data: pd.DataFrame) -> pd.DataFrame:
        """

        Params:
            report_data: Data to be lemmatized. Ideally, this data should have punctuation removed.
                        NOTE: This method can modify this value.

        Returns:
            The lemmatized data.
        """
        descriptions = report_data[_ColName.DESC]
        lemmatized_descriptions = []
        # loop to lemmatize
        for description in descriptions:
            # tokenize to input each word into lemmatize function
            tokens = description.split()
            # returns tuple of (token, nltk_tag)
            tokens_tagged = pos_tag(tokens)
            for i in range(len(tokens)):
                token, token_tag = tokens_tagged[i][0], self.nltk_to_wordnet(
                    tokens_tagged[i][1])
                if token_tag:
                    # only lemmatize if matching POS tag is found
                    tokens[i] = self.lemmatizer.lemmatize(token, token_tag)

            lemmatized_descriptions.append(" ".join(tokens))

        report_data[_ColName.DESC] = lemmatized_descriptions
        return report_data
