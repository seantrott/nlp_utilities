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

	def compare_form_and_meaning(self, words):
		"""Find all pairwise similarities in WORDS."""
		form_similarities, meaning_similarities = [], []
		w1s, w2s = [], []
		for w1, w2 in itertools.combinations(words, 2):
			form_similarities.append(self.compare_form(w1, w2))
			meaning_similarities.append(self.compare_meaning(w1, w2))
			w1s.append(w1)
			w2s.append(w2)
		return {'form': form_similarities,
				'meaning': meaning_similarities,
				# 'is_homophone': is_homophone,
				'w1': w1s,
				'w2': w2s}

