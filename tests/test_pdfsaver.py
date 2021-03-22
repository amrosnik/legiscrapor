import glob 
from legiscrapor import nlpIE
from legiscrapor import pdf_saver as ps 
import pandas as pd 
from os.path import join 

"""
keywords = ['legal aid','judicial assistance']
example_law_files = []
for ext in ('*.doc','*.docx','*.pdf'):
    example_law_files.extend(glob.glob(join('./src/legiscrapor/data/pdfsaver_docs/',ext)))

df = pd.DataFrame()
i = 0 

for law in example_law_files:
    print('**********'+law+'*********')
    text = ps.get_text(law)
    df.loc[i,'Legislation'] = text
    df.loc[i,'Example_number'] = i + 1
    i += 1

matches = nlpIE.full_nlp_ie(df,keywords,'English',1)
"""
