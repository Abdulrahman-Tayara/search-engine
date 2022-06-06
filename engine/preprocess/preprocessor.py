import re
import string
from typing import Callable

import emoji
import numpy as np
from nltk import tokenize, pos_tag
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from num2words import num2words

from engine.preprocess.lemmatizer import LemmatizerWithPOSTagger


class TextPreprocessor():

    def __init__(self, tokenizer: Callable = None) -> None:
        self.tokenizer = tokenizer

        if self.tokenizer is None:
            self.tokenizer = tokenize.word_tokenize

        self.stopwords_tokens = stopwords.words('english')
        self.stemmer = PorterStemmer()
        self.lemmatizer = LemmatizerWithPOSTagger()

    def to_lower(self, text: str) -> str:
        return str(np.char.lower(text))

    def remove_urls(self, text: str) -> str:
        return re.sub("http[^\s]*", "", text, flags=re.IGNORECASE)

    def remove_numbers(self, text: str) -> str:
        return re.sub(r"\d+|[\u0660-\u0669]+", " ", text)

    def convert_numbers(self, text: str) -> str:
        tokens = self.tokenizer(text)
        new_text = ""
        for w in tokens:
            try:
                w = num2words(int(w))
            except:
                a = 0
            new_text = new_text + " " + w
        new_text = np.char.replace(new_text, "-", " ")
        return str(new_text)

    def remove_emojis(self, text: str) -> str:
        return emoji.replace_emoji(text, replace='')

    def remove_punctuation(self, text: str) -> str:
        return text.translate(str.maketrans(' ', ' ', string.punctuation))

    def remove_whitespaces(self, text: str) -> str:
        return text.replace('\\r', ' ').replace('\\n', ' ').replace('\\r\\n', ' ')

    def remove_stop_words(self, text: str) -> str:
        stop_words = stopwords.words('english')
        words = self.tokenizer(text)
        new_text = ""
        for w in words:
            if w not in stop_words and len(w) > 1:
                new_text = new_text + " " + w
        return new_text

    def remove_apostrophe(self, text: str) -> str:
        return str(np.char.replace(text, "'", " "))

    def stemming(self, text: str) -> str:
        tokens = self.tokenizer(text)
        new_text = ""
        for w in tokens:
            new_text = new_text + " " + self.stemmer.stem(w)
        return new_text

    def lemmatizing(self, text: str) -> str:
        tokens = self.tokenizer(text)
        tagged_tokens = pos_tag(tokens)
        new_text = ""
        for token, tag in tagged_tokens:
            new_text = new_text + " " + \
                       self.lemmatizer.lemmatize(token, tag)
        return new_text

    def preprocess(self, text: str) -> str:
        operations = [
            # self.remove_whitespaces,
            self.to_lower,
            self.remove_punctuation,
            self.remove_apostrophe,
            self.remove_stop_words,
            # self.convert_numbers,
            self.stemming,
            self.lemmatizing,
        ]

        new_text = text
        for op in operations:
            new_text = op(new_text)

        return new_text
