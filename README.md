# Tandem
DH Project to analyze text and images in one interface

TandemText.py takes input from the use to identify a folder containing one or more image 
files. The program processes all of the image files through the Tesseract OCR engine and 
outputs TXT files in the NLTK DATA folder

Nltktest2 is under development and can generate basic statistics on a hardcoded TXT file.
It will be expanded to generate additional stats and to loop through the folder containing
TandemText output. Statistics will be written to a CSV file and/or a SQLlite DB

Flaskr
Is a sample program to exercise the Flask web framework for Python.




SETUP
Mac's come with Python. I would suggest you work with that version unless issues arise.

XCOCDE
It's recommended by lots of sites to install XCode. It's unclear to me at the moment what
XCode gives you, but it's an easy install. Here is the link:
https://developer.apple.com/xcode/downloads/


NLTK SET UP
For help outside of these notes go to http://nltk.org

First launch terminal which is your command line interface.
These steps are all commands you type at the command line prompt except for
the first which a hyperlink. You type the text after the word run in each line.
Install Setuptools: http://pypi.python.org/pypi/setuptools
Install Pip: run sudo easy_install pip
Install Numpy: run sudo pip install -U numpy
Install NLTK: run sudo pip install -U nltk


Now Test to see if your installation worked:
run python then type import nltk
Success will be if no errors are displayed after the import command.

Get out Python by CTl-D

GETTING AND RUNNING TANDEM CODE
Just press the Download Zip button at the right side of the page listing the files.

TESSERACT SETUP
I followed these instructions. https://code.google.com/p/python-tesseract/wiki/HowToCompileForHomebrewMac
They are pretty nasty so take your time.


