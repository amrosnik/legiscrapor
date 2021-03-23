import pytest 
from legiscrapor.legisweb_class import legisWeb 
import os 

@pytest.fixture
def eng_web():
    '''Returns a LegisWeb instance with English as the language'''
    return legisWeb()

def test_language(eng_web):
    assert eng_web.language == "English"

def test_set_language(eng_web):
    eng_web.change_language("French")
    assert eng_web.language == "French"

def test_mincount(eng_web):
    assert eng_web.mincount == 1

def test_set_mincount(eng_web):
    eng_web.change_mincount(5)
    assert eng_web.mincount == 5

def test_country(eng_web):
    assert eng_web.country == "GENERIC"

def test_set_country(eng_web):
    eng_web.change_country("Australia")
    assert eng_web.country == "Australia"

def test_read_inputs(eng_web):
    eng_web.read_inputs("./src/legiscrapor/data/testing_input.txt",notTesting=False)
    assert eng_web.inputs[0] == "/home/yourname/chromedriver"
    assert eng_web.country == "Kenya" 
    assert eng_web.downloadPath == "/home/yourname/Downloads/legiscrapor_test/"
    assert eng_web.website == "http://kenyalaw.org/kl/"
    assert eng_web.language == "English"
    assert eng_web.keywords == ["legal aid", "judicial assistance", "legal assistance", "legal service"]
    assert eng_web.webpage == 1

