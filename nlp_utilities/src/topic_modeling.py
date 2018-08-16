"""Wrappers for doing quick topic model extraction."""

import pandas as pd
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import LatentDirichletAllocation, TruncatedSVD
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


class Tokenizer(object):
    """Tokenize (and optionally lemmatize)."""

    def __init__(self, language='english', lemmatize=True):
        """Init."""
        self.lemmatizer = WordNetLemmatizer()
        self.lemmatize = lemmatize

    def preprocess(self, doc):
        """Tokenize and preprocess doc."""
        if self.lemmatize:
            return [self.lemmatizer.lemmatize(word) for word in nltk.word_tokenize(doc)]
        return nltk.word_tokenize(doc)

    def __call__(self, doc):
        """Lemmatize and tokenize doc."""
        return self.preprocess(doc)


class TopicModeler(object):
    """Base class for doing topic modeling."""

    def __init__(self, num_topics=10, language='english', lemmatize=True, max_df=.5, min_df=1, vectorizer_name='tfidf', transformer_name='lsa'):
        """Init."""
        self.language = language
        self.num_topics = num_topics
        self.lemmatize = lemmatize
        self.max_df = max_df
        self.min_df = min_df
        self.tokenizer = Tokenizer(language, lemmatize)
        self.vectorizer_name = vectorizer_name
        self.vectorizer = None
        self.transformer_name = transformer_name
        self.transformer = None

    def _get_topic_labels(self, feature_names, dimensions, top_words=3):
        """Get labels for each dimension of a trained topic model, using original list of feature names.

        Parameters
        ----------
        feature_names: numpy.array
          list of original feature names from vectorizer
        dimensions: list
          matrix of factor loadings for each dimension
        top_words: int
          number of features to select from each model component

        Returns
        -------
        list
          list of len(dimensions), with aggregated feature labels for each dimension.
        """
        return [' '.join(feature_names[np.argsort(dimension)[-top_words:]]) for dimension in dimensions]

    def _load_vectorizer(self, vectorizer_name='tfidf'):
        """Load vectorizer."""
        mappings = {'tfidf': TfidfVectorizer,
                    'count': CountVectorizer}

        return mappings[vectorizer_name](
             max_df=self.max_df, min_df=self.min_df, stop_words=self.language, tokenizer=self.tokenizer)

    def _load_transformer(self, transformer_name):
        """Load transformer (LSA vs. LDA)."""
        mappings = {'lsa': TruncatedSVD,
                    'lda': LatentDirichletAllocation}
        return mappings[transformer_name](n_components=self.num_topics)

    def vectorize_documents(self, documents, fit=True):
        """Vectorize documents."""
        if self.vectorizer is None:
            self.vectorizer = self._load_vectorizer(self.vectorizer_name)
        if fit:
            try:
                self.vectorizer.fit(documents)
            except Exception as e:
                self.vectorizer = None
                raise e
        return self.vectorizer.transform(documents)

    def fit(self, documents):
        """Fit documents using topic model."""
        if self.transformer is None:
            self.transformer = self._load_transformer(self.transformer_name)
        vectorized_text = self.vectorize_documents(documents)
        self.transformer.fit(vectorized_text)

    def transform(self, documents):
        """Transform documents using topic model."""
        if self.transformer is None:
            raise Exception("Model not yet fit. First call TopicModeler.fit(...).")
        vectorized_text = self.vectorize_documents(documents, fit=False)
        transformed = self.transformer.transform(vectorized_text)
        labels = self._get_topic_labels(np.array(self.vectorizer.get_feature_names()), self.transformer.components_)
        return pd.DataFrame(transformed, columns=labels)
        # return self.transformer.transform(vectorized_text)

    def fit_transform(self, documents):
        """Fit and transform documents."""
        self.fit(documents)
        return self.transform(documents)
