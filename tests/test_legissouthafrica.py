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

def test_search_legislation(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa" 
    constit_href = za_web.search_legislation("The Constitution")
    assert constit_href == "https://www.parliament.gov.za/constitutional-amendments"

def test_search_mandates(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    links = za_web.search_mandates('service',za_web.downloadPath) 
    links.sort()
    expected = ['/storage/app/media/Docs/fin_man/329848_1.pdf', '/storage/app/media/Docs/fin_man/329850_1.pdf', '/storage/app/media/Docs/fin_man/329851_1.pdf']
    expected.sort()
    assert len(links) == 3
    assert links == expected

#def test_get_pdfs(za_web):

   

