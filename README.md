# NLP Utilities

Library with utility functions and wrapper classes to perform various NLP functions, including:
* [Document Cleaning](#document-cleaning)
* [Topic modeling](#topic-modeling)
* [Computational Linguistics](#computational-linguistics)

## Installing

For now, you'll need to clone or download the repo, using:

```git clone https://github.com/seantrott/nlp_utilities.git```

Then add `nlp_utilities` to your `PYTHONPATH`, replacing `DIR` with the path to whatever directory `nlp_utilities` is stored in.

```export PYTHONPATH="{DIR}/nlp_utilties":$PYTHONPATH```

## Using NLP Utilities

### Document Cleaning

The `TextCleaner` module has several simple scripts for cleaning and tokenizing documents for the purpose of topic modeling, sentiment analysis, word2vec modeling, and more.

Under the hood this mostly consists of `BeautifulSoup`, `regex`, and `nltk`, but the purpose of `TextCleaner` is to bundle all these together for easy use.

```
from nlp_utilities import TextCleaner

text = '<b>Webpage title.</b>Something else http://somelink.com www.link link.org'
TextCleaner.remove_hyperlinks(text)
TextCleaner.strip_html(text)
```

Or use the `TextCleaner.clean(...)` utility method to bundle these methods into a single call:

```
TextCleaner.clean(text)
```

#### Preprocessing

You can also turn a document into a list of word tokens using `tokenize_words`. This requires instantiating `TextCleaner`.

```
tc = TextCleaner()
tc.tokenize_words('the quick brown fox', remove_stops=True)
```


### Topic Modeling

NLP Utilities has a wrapper class for topic modeling, using either Latent Semantic Analysis (LSA) or Latent Dirichlet Allocation (LDA). Using either is straightforward:

```
from nlp_utilities import TopicModeler

example_documents = ['the cat ate the mouse',
                     'the man ate the pie',
                     'birds like to eat pies',
                     'the bird ate the mouse']
tm = TopicModeler(transformer_name='lsa', num_topics=3)

tm.fit(example_documents)
topics = tm.transform(example_documents)

```

Instead of using `fit` and `transform` separately, you can also use `fit_transform` directly:

```
topics = tm.fit_transform(example_documents)
```

These topics could be used for a number of tasks, including **document classification**.


### Computational linguistics

There are also several utility methods (and classes) for doing work related to computational linguistics:

#### Finding minimal pairs / sets

Given a list of words, one might want to know the **minimal sets** that appear in that list: groups of words that differ only by one sound (or one character).

There are two methods that could be used for this, depending on whether you want your output grouped in terms of **minimal pairs** or **minimal sets**:

```
from nlp_utilities.compling import CorpusUtilities

test_words = ['dog', 'wog', 'fool', 'cool', 'cook', 'sog']
CorpusUtilities.get_minimal_orthographic_pairs(test_words)
CorpusUtilities.get_minimal_orthographic_sets(test_words)
```

#### Getting syllable structure

Given a phonetic transcription of words (or sentences) with syllables marked, it might be useful to break each syllable down into its components. Note that this requires a Regex-formatted string containing the possible **nuclei** that can occur in this mode of phonetic transcription; the default uses the CELEX transcription.

```
from nlp_utilities.compling import CorpusUtilities

example_word = 'lip'  # CELEX transcription for "leap"
CorpusUtilities.get_syllable_components(example_word)
```

#### Comparing the form and meaning distances of words

Given a list of words, you might also want to compare how each pair of words differs in form and meaning.

Here, you can use the `SystematicityUtilities` class. Assuming you have a pretrained `word2vec` model on your computer, you can pass that model into the class, then use the `compare_form_and_meaning` function. By default, the class uses Levenshtein distance as its *form metric*, and *cosine distance* (in the `word2vec` model) as its *meaning metric*, but alternative comparators can be passed in.

```
from nlp_utilities.compling import SystematicityUtilities

systematicity_utils = SystematicityUtilities(model)
comparisons = systematicity_utils.compare_form_and_meaning(words)
```

(Where `model` is a pretrained `word2vec` model, and `words` is a list of strings.)

## To do

Add utilities for:
* Sentiment analysis
* LWIC

Compling utilities:
* Find out whether words rhyme
* Maybe store CMU, CELEX, or another standard pronunciation database with CorpusUtilities --> then this could be used automatically to construct training data, find rhymes, etc.

Add tests.
