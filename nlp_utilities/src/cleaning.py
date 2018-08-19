"""Utilities for cleaning text."""

import re

from nltk import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from bs4 import BeautifulSoup


class TextCleaner(object):
    """Removes html, hyperlinks, etc."""

    def __init__(self, language='english', stops=None):
        self.language = language
        self.stopwords = self._load_stops(stops=stops)

    def _load_stops(self, stops):
        """Load stopwords."""
        return stops or stopwords.words(self.language)

    @classmethod
    def normalize_spacing(cls, text):
        """If punctuation is followed by non-whitespace character, insert space."""
        text = re.sub(r'\.(?=[^ \W\d])', '. ', text)
        text = re.sub(r'\!(?=[^ \W\d])', '! ', text)
        text = re.sub(r'\?(?=[^ \W\d])', '? ', text)
        text = re.sub(r'\,(?=[^ \W\d])', ', ', text)
        return text.strip()

    @classmethod
    def remove_hyperlinks(cls, text):
        """Remove hyperlinks from text."""
        endings = ['\.com', '\.org', '\.edu', '\.net', '\.gov', '\.eu', '\.us']
        substitution = r'http\S+|ftp\S+|www\.\S+'
        for end in endings:
            substitution += '|\S+{r}'.format(r=end)
        return re.sub(substitution, '', text)

    @classmethod
    def strip_html(cls, text):
        """Strip html."""
        cleaned = BeautifulSoup(text, 'lxml')
        return cleaned.text

    def tokenize_words(self, text, remove_stops=True):
        """Word-tokenize document."""
        if remove_stops:
            return [w for w in word_tokenize(text) if w not in self.stopwords]
        return [w for w in word_tokenize(text)]

    @classmethod
    def clean(cls, text, remove_links=True, normalize_space=True):
        """Clean text."""
        cleantext = cls.strip_html(text)
        if remove_links:
            cleantext = cls.remove_hyperlinks(cleantext)
        if normalize_space:
            cleantext = cls.normalize_spacing(cleantext)
        return cleantext.strip()