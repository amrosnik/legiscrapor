import spacy 
import pandas as pd 
import glob
import re 
import numpy as np 
import os

######## ######## ######## ########
######## NLP INFORMATION EXTRACTION MODULE ########
######## ######## ######## ######## 

## lots borrowed from git jists in 
## https://www.analyticsvidhya.com/blog/2020/06/nlp-project-information-extraction/ 
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def load_lang_model(lang): 
    ## pick the correct spacy NLP library
    global nlp 
    if lang == "English":
        try:
            nlp = spacy.load('en_core_web_sm', disable=['ner', 'textcat'])
        except OSError:
            print("Missing spacy module, attempting download.")
            os.system('python3 -m spacy download en_core_web_sm')
            os.system('python -m spacy download en_core_web_sm') # in case the above command doesn't work...
            nlp = spacy.load('en_core_web_sm', disable=['ner', 'textcat'])
    else: 
        raise ValueError("ERROR: CODE CURRENTLY DOES NOT SUPPORT LANGUAGES OTHER THAN ENGLISH") 

### first, let's import some manually created text file, for the most initial proof of concept.
## then, clean it up + put into tabular form 
# function to preprocess legislation docs
def clean(text):
    
    # removing paragraph numbers
    text = re.sub('[0-9]+.\t','',str(text))
    # removing new line characters
    text = re.sub('\n ','',str(text))
    text = re.sub('\n',' ',str(text))
    # removing apostrophes
    text = re.sub("'s",'',str(text))
    # removing hyphens
    text = re.sub("-",' ',str(text))
    text = re.sub("— ",'',str(text))
    # removing quotation marks
    text = re.sub('\"','',str(text))
    # removing salutations
    text = re.sub("Mr\.",'Mr',str(text))
    text = re.sub("Mrs\.",'Mrs',str(text))
    # removing any reference to outside text
    text = re.sub("[\(\[].*?[\)\]]", "", str(text))
    
    return(text)

def sentences(text):
   ## split sentences and questions
   text = re.split('[.?]',text)
   clean_sent = []
   for sent in text:
      clean_sent.append(sent)
   return(clean_sent)

# rule to extract keywords
def sent_subtree(text,patterns):
    # pattern match for schemes or initiatives
    ## patterns = list of keywords.

    schemes = []
    doc = nlp(text)
    flag = 0
    # if no keyword present in sentence
    for token in doc:
        for pat in patterns:
            if re.search(pat, text, re.IGNORECASE) != None:
                flag = 1
                word = ''
                # iterating over token subtree
                for node in token.subtree:
                    word += node.text+' '
                if len(word)!=0:
                    schemes.append(word)
    return(schemes)

''' deprecated, but may be useful eventually ''' 
"""
def plain_text_full_nlp_ie(path):
   ## Function that puts it all together.
   ## path: path to files to examine
   ## the files should be plain text files. 

   ## search for legal aid keywords
   files = glob.glob(path+'*txt')
  
   ## dummy text that should yield empty results: 
   ##files = glob.glob('./dummy_text/*txt')

   df = pd.DataFrame()
   i=0
   for file in files: 
      with open(file,encoding='utf8') as f:
         df.loc[i,'Legislation'] = f.read()
         df.loc[i,'Example_number'] = i + 1
         i += 1 

   full_nlp_ie(df)
"""

def full_nlp_ie(df,keywords,language,mincount):
   ## Function that puts it all together.

   ## NOTE: df is a pandas DataFrame following the conventions 
   ## of pdf_saver.scan_pdfs() output!!!  

   # preprocessing legislation text
   df['Legislation_clean'] = df['Legislation'].apply(clean)
   df['sentences'] = df['Legislation_clean'].apply(sentences)

   ## create new dataframe where each row is a different sentence,
   ## with new column displaying sentence character length
   df2 = pd.DataFrame(columns=['File_name','sent','example_num','len'])

   row_list = []

   for i in range(len(df)):
       for sent in df.loc[i,'sentences']:
           wordcount = len(sent.split())
           year = df.loc[i,'Example_number']
           file_name = df.loc[i,'File_name']
           dict1 = {'file_name':file_name,'example_num':year,'sent':sent,'len':wordcount}
           row_list.append(dict1)

   df2 = pd.DataFrame(row_list)
   load_lang_model(language) # load in our NLP model for language of choice
   df2['Schemes'] = df2['sent'].apply(sent_subtree,patterns=keywords)

   example_nums = df2['example_num'].unique().astype(int)

   match_file_names = []
   for i in example_nums: 
      non_empty_schemes = df2[df2['Schemes'].map(lambda d: len(d)) > 0]
      count = len(non_empty_schemes.loc[non_empty_schemes['example_num'] == i])
      #print(non_empty_schemes.loc[non_empty_schemes['example_num'] == i]['sent'])
      if count > mincount: 
          print("***** There is a good chance document # "+str(i)+" is a relevant document. *****")
          match_file_names.append(non_empty_schemes.loc[non_empty_schemes['example_num'] == i]['file_name'].tolist())

   match_file_names = [item for sublist in match_file_names for item in sublist]
   match_file_names = np.unique(match_file_names)
   return(match_file_names)

