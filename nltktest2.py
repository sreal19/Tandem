__author__ = 'sbr'
from nltk.corpus import PlaintextCorpusReader
corpus_root = 'tessyout'
wordlists = PlaintextCorpusReader(corpus_root, '.*')
print wordlists.fileids()
print wordlists.words('4_outofthewoods.txt')



