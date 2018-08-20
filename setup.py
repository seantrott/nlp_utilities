from setuptools import setup, find_packages

long_description = \
"""
Utilities for NLP needs.
"""

setup(
    name = 'lisc',
    description = 'NLP Utilities',
    long_description = long_description,
    author = 'Sean Trott',
    author_email = 'sttrott@ucsd.edu',
    url = 'https://github.com/seantrott/nlp_utilities',
    packages = find_packages(),
    license = 'TODO',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
    download_url = 'https://github.com/seantrott/nlp_utilities',
    keywords = ['nlp', 'text-mining'],
    install_requires = ['numpy', 'nltk', 'bs4', 'sklearn', 'pandas', 'editdistance']
)
