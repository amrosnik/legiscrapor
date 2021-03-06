import pytest 
from legiscrapor.nlpIE import *
import os 
import re 
import legiscrapor.pdf_saver as ps
import shutil 

#### UNIT TESTS FOR NLPIE MODULE #### 
## Each unit test name roughly corresponds to 
## the function it is testing. 

@pytest.fixture
def text_example():
    ''' Returns the text for a legal aid document exerpt.''' 
    with open('./src/legiscrapor/data/legal_aid_examples/legal_aid_example_1.txt', 'r') as f:
        text = f.read()
    return text

def test_no_lang_model():
    ''' Check if we, correctly, get a ValueError from a currently unsupported language'''
    with pytest.raises(ValueError):
        load_lang_model("Mandarin")

def test_lang_model():
    ''' Check if supported language is actually supported'''
    try:
        load_lang_model("English")
    except TestError:
        pytest.fail("Unexpected error in nlpIE.load_lang_model() when loading English language model")

def test_clean(text_example):
    cleaned_text = clean(text_example) 
    assert ('Mr\.' not in cleaned_text)
    assert ('Mrs\.' not in cleaned_text)
    assert ('-' not in cleaned_text)
    assert ('\"' not in cleaned_text)
    assert ("'s" not in cleaned_text)
    assert ("\n" not in cleaned_text)
    assert ("\n " not in cleaned_text)
    assert ( len(re.findall('[0-9]+.\t',cleaned_text)) == 0 )
    assert ( len(re.findall("[\(\[].*?[\)\]]",cleaned_text)) == 0 )

def test_sentences(text_example):
    cleaned_text = clean(text_example) 
    cleaned_sents = sentences(cleaned_text)
    # the expected number of sentences in the doc is 18. 
    assert len(cleaned_sents) == 18

def test_subtree(text_example):
    cleaned_text = clean(text_example) 
    cleaned_sents = sentences(cleaned_text)
    patterns = ["legal aid", "judicial assistance", "legal assistance", "legal service"]
    subs = [sent_subtree(sentence,patterns) for sentence in cleaned_sents ] 

    ## let's check that each sentence of cleaned_sents was tokenized correctly: 
    assert len(subs[0]) == 42
    assert len(subs[1]) == 25
    assert len(subs[2]) == 35
    assert len(subs[3]) == 0
    assert len(subs[4]) == 90
    assert len(subs[5]) == 0
    assert len(subs[6]) == 0
    assert len(subs[7]) == 74
    assert len(subs[8]) == 42
    assert len(subs[9]) == 0
    assert len(subs[10]) == 71
    assert len(subs[11]) == 80
    assert len(subs[12]) == 106
    assert len(subs[13]) == 0
    assert len(subs[14]) == 7
    assert len(subs[15]) == 0
    assert len(subs[16]) == 13
    assert len(subs[17]) == 0

def test_full_nlp():
    # unit tests for full_nlp_ie() 
    df = ps.scan_pdfs('./src/legiscrapor/data/pdfsaver_docs/')
    keywords = ["legal aid", "judicial assistance", "legal assistance", "legal service"]
    matches = full_nlp_ie(df,keywords,'English',1)
    # remove temporary files created in processing low-resolution PDFS
    os.remove('./src/legiscrapor/data/pdfsaver_docs/low_resolution_pdfs.txt')
    shutil.rmtree('./src/legiscrapor/data/pdfsaver_docs/temp_images')

    assert len(matches) == 4

def test_no_nlp():
    # unit tests for full_nlp_ie(), to ensure full_nlp_ie() returns correct output for an empty text DataFrame 
    df = ps.scan_pdfs('./src/legiscrapor/data/legal_aid_examples/')
    keywords = ["legal aid", "judicial assistance", "legal assistance", "legal service"]
    matches = full_nlp_ie(df,keywords,'English',1)

    assert len(matches) == 0

def test_spanish():
    ''' Trying the search_for_keywords() paradigm with Spanish language, 
    mostly to check that special characters are detected as unique '''
    keywords = ['gobierno','Espana','España'] 
    df = ps.scan_pdfs('./src/legiscrapor/data/selsearch_nlp_docs/')
    matches = full_nlp_ie(df,keywords,'Spanish',1)
    assert len(matches) == 1 # the only match should be the Gobierno de España wikipedia PDF.

