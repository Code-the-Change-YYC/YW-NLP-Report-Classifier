from typing import Optional
import re

import spacy
spacy.prefer_gpu()


class Scrubber:
    """Detector that will run through descriptions and detect sensitive data such as names, numbers and time.

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
    # names and initials
    name_labels = {"PERSON", "ORG", "GPE"}
    # number
    number_labels = {"CARDINAL"}
    # time
    time_labels = {"TIME"}
    nlp = spacy.load("en_core_web_lg",
                     disable=['tokenizer', 'parser', 'tagger'])

    def __init__(self, client_tokens, ent_replacement: str = None):
        self.replacement_method = ent_replacement
        self.client_tokens = client_tokens

    def scrub(self, text: str):
        scrubbed_text = []
        # run model over the description
        for doc in self.nlp.pipe([text]):
            for token in doc:
                if token.text.lower() in Scrubber.whitelisted_words:
                    scrubbed_text += token.text
                elif token.text in self.client_tokens or token.ent_type_ in Scrubber.name_labels:
                    if self.replacement_method:
                        scrubbed_text.append(self.replacement_method)
                    else:
                        scrubbed_text.append("{{NAME}}")
                elif token.ent_type_ in Scrubber.number_labels:
                    scrubbed_text.append("{{NUMBER}}")
                elif token.ent_type_ in Scrubber.time_labels:
                    scrubbed_text.append("{{TIME}}")
                else:
                    scrubbed_text.append(token.text)

        return " ".join(scrubbed_text)
