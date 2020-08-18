from typing import Optional
import re

import spacy


class NameDetector:
    """Detector that will run through descriptions and detect sensitive data such as names.


    Upon initialization loops through whitelisted words to append to disallowed nouns, so non-sensitive data
    isn't unnecessarily scrubbed.
    """
    replacement_method: Optional[str]
    # List of words that should remain unscrubbed
    # Note: These are converted to lower case anyways
    whitelisted_words = [
        "Staff",
        "EMS",
        "Fire",
        "CPS",
        "Rockyview",
        "Rocky",
        "View",
        "Health",
        "Link",
        "Sheldon",
        "Gabapentin",
        "Chumir",
        "Hospital",
        "Fentanyl",
        "Writer",
        "Crystal",
        "Meth",
        "Overdose",
        "Police",
        "Client",
        "First",
        "Aid",
        "Providence",
    ]
    whitelisted_words = [w.lower() for w in whitelisted_words]

    # Spacy's entity labels to be removed
    name_labels = {"PERSON", "ORG", "GPE"}

    def __init__(self, client_tokens, ent_replacement: str = None):
        self.replacement_method = ent_replacement
        self.client_tokens = client_tokens

        spacy.prefer_gpu()
        # load the model
        self.nlp = spacy.load("en_core_web_lg")

    def scrub(self, text: str):
        # run model over description
        doc = self.nlp(text)
        for ent in doc.ents:
            whitelisted = ent.text.lower() in NameDetector.whitelisted_words
            if (ent.label_ in NameDetector.name_labels or ent.text in self.client_tokens) and not whitelisted:
                text = text[:ent.start_char] + ('*' * len(ent.text)) + text[ent.end_char:]

        # run model again to ignore asterisks
        doc = self.nlp(text)
        # iterate over tokens to catch rest of initials
        for i, token in enumerate(doc):
            if token.text in self.client_tokens and token.text.lower() not in NameDetector.whitelisted_words:
                # convert to span to get start_char and end_char attributes
                span = doc[i:i + 1]
                text = text[:span.start_char] + ('*' * len(token.text)) + text[span.end_char:]

        if self.replacement_method:
            text = re.sub(r'[*]+', self.replacement_method, text)

        return text
