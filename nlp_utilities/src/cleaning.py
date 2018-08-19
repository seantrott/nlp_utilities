"""Utilities for cleaning text."""

import re

from bs4 import BeautifulSoup


class TextCleaner(object):
	"""Removes html, hyperlinks, etc."""

	def __init__(self, language='english'):
		self.language = language

	def remove_hyperlinks(self, text):
		"""Remove hyperlinks from text."""
		endings = ['\.com', '\.org', '\.edu', '\.net', '\.gov', '\.eu', '\.us']
		substitution = r'http\S+|ftp\S+|www\.\S+'
		for end in endings:
			substitution += '|\S+{r}'.format(r=end)
		return re.sub(substitution, '', text)

	def strip_html(self, text):
		"""Strip html."""
		cleaned = BeautifulSoup(text, 'lxml')
		return cleaned.text

	def clean(self, text, remove_links=True):
		"""Clean text."""
		cleantext = self.strip_html(text)
		if remove_links:
			cleantext = self.remove_hyperlinks(cleantext)
		return cleantext.strip()