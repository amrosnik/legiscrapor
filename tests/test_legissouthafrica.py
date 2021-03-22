import pytest 
from legiscrapor.legissouthafrica import legisSouthAfrica
import os 

@pytest.fixture
def za_web():
    '''Returns a LegisSouthAfrica instance'''
    return legisSouthAfrica()

def test_language(za_web):
    assert za_web.language == "English"

def test_country(za_web):
    assert za_web.country == "South Africa"


