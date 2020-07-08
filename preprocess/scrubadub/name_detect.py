import scrubadub


class CustomNameDetector(scrubadub.detectors.NameDetector):
    """Detector that will run through descriptions and detect sensitive data such as names.


    Upon initialization loops through whitelisted words to append to disallowed nouns, so non-sensitive data
    isn't unnecessarily scrubbed.
    """
    # Custom scrubadub logic
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

    def __init__(self):
        for word in self.whitelisted_words:
            self.disallowed_nouns.add(word)
