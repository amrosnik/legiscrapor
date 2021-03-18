import pytest 
from legiscrapor.legisWeb import * 

def test_language():
    eng_web = legisWeb()
    assert eng_web.language == "English"

def test_set_language()
    eng_web = legisWeb()
    eng_web.change_language("French")
    assert eng_web.language == "French"

def test_mincount():
    eng_web = legisWeb()
    assert eng_web.mincount == 1

def test_set_mincount()
    eng_web = legisWeb()
    eng_web.change_mincount(5)
    assert eng_web.mincount == 5

def test_country():
    eng_web = legisWeb()
    assert eng_web.country == "GENERIC"

def test_set_country()
    eng_web = legisWeb()
    eng_web.change_country("Australia")
    assert eng_web.country == "Australia"


