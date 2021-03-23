import pytest 
from legiscrapor.nlpIE import *
import os 
import re 

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
