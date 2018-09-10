"""Class with utility functions for comparing the forms and meanings of words

By default, uses Levenshtein distance and cosine similarity (from a trained word2vec model),
but can also use custom form/meaning metrics.
"""

import editdistance as ed

import itertools
import os


class SystematicityUtilities(object):

    def __init__(self, model=None, form_metric=None, meaning_metric=None):
        """Initialize class with specified form/meaning comparators.

        Parameters
        ----------
        model: KeyedVectors
          object with word embeddings
          alternatively, could be a wordnet / framenet model
        form_metric: function
          function to compare words along form dimension
          if None, defaults to Levenshtein distance
        meaning_metric: function
          function to compare words along meaning dimension
          if none, defaults to cosine distance
        """
        if form_metric is not None:
            self.compare_form = form_metric
        if meaning_metric is not None:
            self.compare_meaning = meaning_metric
        self.model = model


    def compare_form(self, w1, w2):
        """Compare the similarity in forms between w1 and w2.

        Parameters
        ----------
        w1: str
          the first wordform to be compared
        w2: str
          the second wordform to be compared

        Returns
        -------
        float
          metric of similarity(w1, w2)
        """
        return ed.eval(w1, w2)

    def compare_meaning(self, w1, w2):
        """Compare similarity in meaning between w1 and w2.


        Parameters
        ----------
        w1: str
          the first meaning to be compared
        w2: str
          the second meaning to be compared

        Returns
        -------
        float
          metric of meaning similarity(w1, w2)
        """
        return self.model.similarity(w1, w2)

    def _compare_form_and_meaning(self, row, w1_column, w2_column):
        w1, w2 = row[w1_column], row[w2_column]
        return (self.compare_form(w1, w2), self.compare_meaning(w1, w2))

    def compare_form_and_meaning_df(self, df, w1_column, w2_column):
        """Find all pairwise similarities in dataframe."""
        comparisons = df.apply(self._compare_form_and_meaning, w1_column=w1_column, w2_column=w2_column, axis=1)
        zipped = list(zip(*comparison))
        forms, meanings = zipped[0], zipped[1]
        dataframe['form'] = forms
        dataframe['meaning'] = meanings
        return dataframe

