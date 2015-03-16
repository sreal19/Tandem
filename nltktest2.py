

import nltk.data
import os
from nltk.corpus import stopwords
from nltk.corpus.reader import WordListCorpusReader
from nltk.corpus import PlaintextCorpusReader
from nltk.tokenize import word_tokenize


container = nltk.data.load('corpora/ocrout_corpus2/BookScanCenter_9.txt',format='raw')

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


english_stops = set(stopwords.words('english'))

words = ["Can't", 'is', 'a', 'contraction']
stopsout = [word for word in words if word not in english_stops]
#print stopsout


reader = WordListCorpusReader('/Users/sbr/nltk_data/corpora/ocrout_corpus2', ['BookScanCenter_9.txt'])
#print "reader.words", reader.words()
#print reader.fileids()





corpus_root = '/Users/sbr/nltk_data/corpora/ocrout_corpus2'
file = 'BookScanCenter_9.txt'
#files = [ f for f in os.listdir(corpus_root) if os.path.isfile(os.path.join(corpus_root,f)) ]
#for file in files:
reader = WordListCorpusReader(corpus_root, file)

#reader.words seems to return a list containing the lines in the poem
chunks = reader.words()

item_count = 0
total_chars = 0
word_count = 0
wordlist = []
for item in chunks:
    print "count=", item_count
    print chunks[item_count]
    total_chars += len(chunks[item_count])
    w_tokens = word_tokenize(chunks[item_count])
    word_count += len(w_tokens)
    item_count += 1
    for word in w_tokens:
        wordlist.append(word)


print "count=", word_count
print "total characters=", total_chars
avg_word_length = float(total_chars)/float(word_count)
print "average word length=", avg_word_length
print sorted(wordlist)

#print wordlists.fileids()
print len()
#sentences = tokenizer.tokenize('BookScanCenter_9.txt')


''' sample code
import nltk

corpus = nltk.corpus.reader.plaintext.PlaintextCorpusReader(".", "news1.txt")

print "ACCESSING PARAGRAPHS"

paragraphs=corpus.paras()

for p in paragraphs:
    print p

raw_input()

print "ACCESSING SENTENCES"

sentences=corpus.sents()

for s in sentences:
    print s

raw_input()

print "ACCESSING WORDS"

words=corpus.words()

for w in words:
    print w
'''