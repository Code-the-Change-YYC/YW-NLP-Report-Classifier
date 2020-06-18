import spacy, re
import pandas as pd


class Spacy_sent_Tokenizer:
    sent: str
    train_model: str

    """
    set up basic instance variables
    size : this class support spacy two english model sets of "en_core_web_lg" and "en_core_web_sm"
    """

    def __init__(self, sent, size="large"):

        self.sent = sent
        if size == "large":
            self.train_model = "en_core_web_lg"
        else:
            self.train_model = "en_core_web_sm"

    """
    The method perform basic cleaning up for text data with spacy
    
    """

    def tokenized_basic(self):

        nlp = spacy.load(self.train_model)
        return [w.lemma_ if w.lemma_ != "-PRON-" else w.text
                for w in nlp(self.sent)
                if not nlp.vocab[w.text].is_stop
                and not w.is_punct
                and not w.is_space
                # and not w.pos_ == "PRON"
                ]

# testing

doc = "data-processed.csv"
pd_doc = pd.read_csv(doc)
t_discription = pd_doc["DESCRIPTION"]

for sent in t_discription[:5]:
    tok = Spacy_sent_Tokenizer(sent,"small")
    print(tok.tokenized_basic())
