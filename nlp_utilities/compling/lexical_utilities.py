"""Utility methods and classes for computational linguistics purposes."""

import itertools
import editdistance as ed

import re


class CorpusUtilities(object):
    """Utility methods for extracting useful statistics from corpora."""

    @classmethod
    def get_minimal_orthographic_sets(cls, words, index=0, verbose=False):
        """Retrieve all minimal sets from input words, as long as their
        orthographic difference is at the correct index.

        Parameters
        ----------
        words: list
          list of strings
        index: integer
          index specifying which characters to compare across words.

        Returns
        -------
        list
          list of lists of strings that differ by one character
        """
        sets, seen = [], []
        for n1, w1 in enumerate(words):
            if verbose:
                print("{index} of {length} words".format(index=n1, length=len(words)))
            w1_pairs = []
            for w2 in words[n1+1:]:
                if w2 not in seen and len(w1) > index and len(w2) > index and ed.eval(w1, w2) == 1 and len(w1) == len(w2) and w1[index] != w2[index]:
                    w1_pairs.append(w1)
                    w1_pairs.append(w2)
                    seen.append(w2)
            if len(w1_pairs) > 0:
                sets.append(list(set(w1_pairs)))
        return sets

    @classmethod
    def get_minimal_orthographic_pairs(cls, words, index=0):
        """Retrieve all minimal pairs from input words, as long as their
        orthographic difference is at the correct index.

        Parameters
        ----------
        words: list
          list of strings
        index: integer
          index specifying which characters to compare across words.

        Returns
        -------
        list
          list of string-pairs that differ by one character
        """
        pairs = []
        for w1, w2 in itertools.combinations(words, 2):
            if len(w1) > index and len(w2) > index and ed.eval(w1, w2) == 1 and len(w1) == len(w2) and w1[index] != w2[index]:
                pairs.append([w1, w2])
        return pairs

    @classmethod
    def get_syllable_components(cls, syllable, nuclei='[5@694{8312i7u$#eqFEIQVU$]|ju'):
        """Split syllable into onset, nucleus, and coda.

        Requires regex code of possible nuclei. Default is CELEX encoding of nuclei
        realizations.

        Parameters
        ----------
        syllable: str
          phonetic transcription of single syllable
        nuclei: str
          regex string with the possible nuclei to split on

        Returns
        -------
        dict
          dictionary with onset, nucleus, and coda
        """
        nucleus = re.findall(nuclei, syllable)
        if len(nucleus) < 1:
            return None
        onset, coda = syllable.split(nucleus[0])
        return {'nucleus': nucleus[0],
                'onset': onset,
                'coda': coda}

    @classmethod
    def is_rhyme(cls, s1, s2):
        """Returns whether syllables rhyme."""
        s1_components, s2_components = cls.get_syllable_components(s1), cls.get_syllable_components(s2)
        return s1_components['nucleus'] == s2_components['nucleus'] and s1_components['coda'] == s2_components['coda']
