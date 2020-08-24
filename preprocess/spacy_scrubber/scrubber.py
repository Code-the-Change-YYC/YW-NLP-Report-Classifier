from typing import Optional
import re

import spacy


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

    def __init__(self, client_tokens, ent_replacement: str = None):
        self.replacement_method = ent_replacement
        self.client_tokens = client_tokens

        spacy.prefer_gpu()
        # load the model
        self.nlp = spacy.load("en_core_web_lg")

    def scrub(self, text: str):
        scrubbed_text = ""
        # run model over the description
        doc = self.nlp(text)
        for token in doc:
            if token.text.lower() in Scrubber.whitelisted_words:
                scrubbed_text += token.text
            elif token.text in self.client_tokens or token.ent_type_ in Scrubber.name_labels:
                if self.replacement_method:
                    scrubbed_text += self.replacement_method
                else:
                    scrubbed_text += "{{NAME}}"
            elif token.ent_type_ in Scrubber.number_labels:
                scrubbed_text += "{{NUMBER}}"
            elif token.ent_type_ in Scrubber.time_labels:
                scrubbed_text += "{{TIME}}"
            else:
                scrubbed_text += token.text
            scrubbed_text += " "

        return scrubbed_text
