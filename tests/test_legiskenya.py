import pytest 
from legiscrapor.legiskenya import legisKenya
import os 

@pytest.fixture
def kl_web():
    '''Returns a LegisKenya instance'''
    return legisKenya()

def test_language(kl_web):
    assert kl_web.language == "English"

def test_country(kl_web):
    assert kl_web.country == "Kenya"


