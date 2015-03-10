
__author__ = 'sr-cv'
'''
TANDEM 0.05
Playing Around with NLTK
Authors: Stephen Real and Christopher Vitale
Follow CVDH4 and SBReal on Twitter and Github
DH Praxis 14-15 CUNY Graduate Center
'''

import csv
import pytesseract
from PIL import Image
import os
import glob
from nltk.corpus import PlaintextCorpusReader

#function captures location of image files
def get_input_folder():
    global good_input
    folder = raw_input('Enter the folder that contains your images: ');
    if os.path.isdir(folder):
        good_input = True
        return folder
    else:
        print ("Folder does not exist!")

#helper function to OCR a singe file
def process_image(file):
    input_image = Image.open(file)
    input_image= input_image.convert('RGB')
    output_data = pytesseract.image_to_string(input_image)
    return output_data

#run the Tesseract OCR engine using the helper function process_image()
def ocrit(file):
    print ("Processing " + file)
    fullpath = infolder + file
    ofile = os.path.splitext(file)[0]
    outfile = infolder + outfolder + '/' + ofile + '.txt'
    temp = open(outfile, 'w')
    temp.write (str(process_image(fullpath)))
    temp.close()

def make_ocr_folder(x):
    outname = 'corpus'
    count = 1
    while True:
        try:
            os.mkdir(x + outname)
            break
        except(OSError):
            outname = 'corpus' + str(count)
            count += 1
    return outname

#capture the folder that contains image files.
good_input = False
while good_input == False:
    infolder = get_input_folder()

#create the output folder
outfolder = make_ocr_folder(infolder)

#loop through the user's input folder and find image files
#for testing purposes only work with PNG files now
outcount = 1
print
print ("processing image files in " + infolder)
print

files = [ f for f in os.listdir(infolder) if os.path.isfile(os.path.join(infolder,f)) ]
for file in files:
    if os.path.splitext(file)[1] == '.tiff':
        ocrit(file)
        outcount += 1
    elif os.path.splitext(file)[1] == '.jpg':
        ocrit(file)
        outcount += 1
    elif os.path.splitext(file)[1] == '.png':
        ocrit(file)
        outcount += 1
    else:
       print
       print (file + " is not an image file. Skipped... ")

'''
#NLTK processing of files output
print
print 'NLTK Step'
print

nltk_in_path = infolder + outfolder
nltk_input_files = os.listdir(nltk_in_path)
print "nltk folder="
print nltk_in_path

doc_text = PlaintextCorpusReader(nltk_in_path, '.*')

print "Word Length"
print
wl_list = []
for file in nltk_input_files:
    nltk_data = [len(doc_text.words(file))]
    print nltk_data
    wl_list.append(nltk_data)

print wl_list
'''
'''
out = csv.writer(open('TANDEM_output.csv','w'), delimiter=',',quoting=csv.QUOTE_ALL)
out.writerow('w')
out.writerow(data1)
out.writerow(data2)
out.writerow(data3)
out.writerow(data4)
out.writerow(data5)
'''

