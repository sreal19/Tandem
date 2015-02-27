__author__ = 'sbr'
import pytesseract
from PIL import Image

def process_image(file):
    input_image = Image.open(file)
    input_image= input_image.convert('RGB')
    output_data = pytesseract.image_to_string(input_image)
    return output_data

#print process_image('tessy.png')

f = open('tessyout/tessyout.txt','w' )
f.write (str(process_image('tessy.png')))
f.close()

