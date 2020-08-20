import re
import string

from tensorflow.keras.layers.experimental.preprocessing import TextVectorization
from tensorflow.strings import lower, regex_replace


def custom_standardization(input_data):
    lowercase = lower(input_data)
    stripped_html = regex_replace(lowercase, "<br />", " ")
    return regex_replace(stripped_html, f"[{re.escape(string.punctuation)}]", "")


if __name__ == "__main__":
    pass
