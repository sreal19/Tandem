__author__ = 'sr-cv'
'''
TANDEM 0.05
Authors: Stephen Real and Christopher Vitale
Follow CVDH4 and SBReal on Twitter and Github
DH Praxis 14-15 CUNY Graduate Center
'''

import csv
import pytesseract
from PIL import Image
import os
from cStringIO import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from nltk.corpus import PlaintextCorpusReader
import nltk.data
from nltk.corpus import stopwords
from nltk.corpus.reader import WordListCorpusReader
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer
import csv

#initialize output file open switch
outputopen = False


'''***********************************************
***                                              *
***     DEFINE ALL THE OCR FUNCTIONS FIRST       *
***                                              *
***********************************************'''


def get_input_folder():         #Capture location of user's image files
    global good_input
    folder = raw_input('Enter the folder that contains your images: ');
    if os.path.isdir(folder):
        good_input = True
        return folder
    else:
        print ("Folder does not exist!")

def process_image(file):            #helper function to OCR a singe file
    input_image = Image.open(file)
    input_image= input_image.convert('RGB')
    output_data = pytesseract.image_to_string(input_image)
    return output_data

def ocrit(fullpath, file):          #run Tesseract OCR engine using process_image()
    ofile = os.path.splitext(file)[0]
    outfile = outpath + outfolder + '/' + ofile + '.txt'
    temp = open(outfile, 'w')
    temp.write (str(process_image(fullpath)))
    temp.close()

def pdfconvert(fullpath, file, pages=None):     #Convert PDF to TXT
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fullpath, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()

    ofile = os.path.splitext(file)[0]
    outfile = outpath + outfolder + '/' + ofile + '.txt'
    text = output.getvalue()
    output.close
    temp = open(outfile, 'w')
    temp.write (text)
    temp.close()

def make_corpus_folder(x):              #Create a folder for the OCR Output/NLTK input
    outname = 'ocrout_corpus'
    count = 1
    while True:
        try:
            os.mkdir(x + outname)
            break
        except(OSError):
            outname = 'ocrout_corpus' + str(count)
            count += 1
            print "could not create folder ", x + outname, "...retrying..."
    return outname

'''***********************************************
***                                              *
***     NOW DEFINE ALL THE NLTK FUNCTIONS        *
***                                              *
***********************************************'''

def tokenize_file(file):            #tokenize input file, count words, characters, remove stopwords
    global english_stops
    tokenizer = RegexpTokenizer(r'\w+')
    item_count = 0
    total_chars = 0
    word_count = 0
    wordlist = []

    item_count = 0
    reader = WordListCorpusReader(corpus_root, file)
    chunks = reader.words()

    for item in chunks:
        total_chars += len(chunks[item_count])
        word_tokens = tokenizer.tokenize(chunks[item_count])
        word_count += len(word_tokens)
        item_count += 1
        for word in word_tokens:
            wordlist.append(word)
    stopsout = [word for word in wordlist if word.lower() not in english_stops]
    return wordlist, stopsout, word_count, total_chars

def build_sorted_ascii(wordlist):       #convert to ascii, lowercase and sort
    i = 0
    templist = []
    for word in wordlist:
        temp = wordlist[i].encode('ascii', 'ignore')
        templist.append(temp.lower())
        i += 1
    sorted_wordlist = sorted(templist)
    return sorted_wordlist

def build_unique_dictionary(inlist):        #find unique words and count them
    unique = [inlist[0].lower()]
    countlist = [1]
    i = 1
    o = 0

    for i in range(1, len(inlist)):
        if inlist[i].lower() == unique[o]:
            countlist[o] += 1
        else:
            unique.append(inlist[i].lower())
            countlist.append(1)
            o += 1
        i += 1
    return unique, countlist

def write_first_row(outname):               #write the first row of the main output file
    global outputopen, file, resultspath

    with open(outname, 'wb') as csvfile:
            tandemwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            tandemwriter.writerow(['File','Total Word Count', 'Total Characters', 'Average Word Length',
                                   'Unique Word Count', 'Count without Stopword'])
            tandemwriter.writerow([file]+[allcount]+[allchar]+[avg_word_length]+[len(unique_nonstop_words)]+
                                  [len(nonstops)])
    outputopen = True
    write_the_lists()

def write_the_rest(outname):                #write subsequent rows of main output file
    global file
    with open(outname, 'a') as csvfile:
            tandemwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            tandemwriter.writerow([file]+[allcount]+ [allchar]+[avg_word_length]+[len(unique_nonstop_words)]+[len(nonstops)])
    write_the_lists()

def write_the_lists():                      #write the wordlists
    #write list of all the words
    words_csv = resultspath + os.path.splitext(file)[0] + '_allwords.csv'
    with open(words_csv, 'wb') as csvfile:
            wlwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            wlwriter.writerow(['All Words'])
            for item in ascii_sorted:
                wlwriter.writerow([item])

    #write a list of unique words with counts other than stop words
    unique_csv = resultspath + os.path.splitext(file)[0] + '_unique.csv'
    with open(unique_csv, 'wb') as csvfile:
            i = 0
            unwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
            unwriter.writerow(['Unique Non Stop Words', 'Count'])
            for i in range (0, len(unique_nonstop_words)):
                unwriter.writerow([unique_nonstop_words[i]]+[nonstop_counts[i]])
                i += 1
'''***********************************************
***                                              *
***     NOW WE GET TO THE MAIN LOGIC             *
***                                              *
***********************************************'''

#capture the folder that contains image files.
good_input = False
while good_input == False:
    infolder = get_input_folder()

#create the output folder
outpath = './'
outfolder = make_corpus_folder(outpath)

#find image files in the folder and convert them to text
outcount = 1
print "\n", "processing image files in " + infolder, "\n"


files = [ f for f in os.listdir(infolder) if os.path.isfile(os.path.join(infolder,f)) ]
for file in files:
    print ("Processing " + file)
    fullpath = infolder + file
    if os.path.splitext(file)[1] == '.tiff':
        ocrit(fullpath, file)
        outcount += 1
    elif os.path.splitext(file)[1] == '.jpg':
        ocrit(fullpath, file)
        outcount += 1
    elif os.path.splitext(file)[1] == '.png':
        ocrit(fullpath, file)
        outcount += 1
    elif os.path.splitext(file)[1] == '.pdf':
        pdfconvert(fullpath, file)
    else:
       print "\n", file + " is not an image file. Skipped... "

''' Now all image files have been converted. Analyze them with nltk'''
print "\n", "starting nltk process ", "\n"

#container = nltk.data.load('corpora/ocrout_corpus2/BookScanCenter_9.txt',format='raw')
#tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
english_stops = stopwords.words('english')
corpus_root = outfolder

files = [ f for f in os.listdir(corpus_root) if os.path.isfile(os.path.join(corpus_root,f)) ]
for file in files:
    if os.path.splitext(file)[1] == '.txt':
        allwords, nonstops, allcount, allchar = tokenize_file(file)
        avg_word_length = round(float(allchar)/float(allcount), 2)
        ascii_sorted = []
        ascii_sorted = build_sorted_ascii(allwords)
        nonstop_sorted = []
        nonstop_sorted = build_sorted_ascii(nonstops)
        unique_nonstop_words, nonstop_counts  = build_unique_dictionary(nonstop_sorted)

        #write the results of nltk process to csv files
        resultspath = './'
        outfile = resultspath + 'tandem' + 'main.csv'
        if outputopen:
            write_the_rest(outfile)
        else:
            write_first_row(outfile)

def merge_all():
    global resultspath

    allfile = resultspath + 'tandem' + '_bigtext.txt'
    with open(allfile, 'w') as outfile:
        for file in files:
            fullname = corpus_root + '/'+ file
            if os.path.splitext(file)[1] == '.txt':
                with open(fullname) as infile:
                    outfile.write(infile.read())
            else:
                print "skipping"




