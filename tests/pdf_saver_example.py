import pdfminer.high_level as ph 
import os
from os.path import join
import pytesseract
from PIL import Image
from wand.image import Image as wandimage
import glob 
import nlpIE
import pandas as pd 
import pdf_saver as ps 

example_law_files = []
for ext in ('*.doc','*.docx','*.pdf'):
    example_law_files.extend(glob.glob(join('../../Documents/WORLD/Examples_of_laws/',ext)))

df = pd.DataFrame()
i = 0 

for law in example_law_files:
    print('**********'+law+'*********')
    text = ps.get_text(law)
    df.loc[i,'Legislation'] = text
    df.loc[i,'Example_number'] = i + 1
    i += 1

nlpIE.legal_aid_nlp_ie(df)
