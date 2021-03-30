import pytest 
from legiscrapor.legissouthafrica import legisSouthAfrica
import os 
import shutil

@pytest.fixture
def za_web():
    '''Returns a LegisSouthAfrica instance'''
    return legisSouthAfrica()

def test_language(za_web):
    assert za_web.language == "English"

def test_country(za_web):
    assert za_web.country == "South Africa"

def test_no_run(za_web):
    ''' Check if we, correctly, get a ValueError from a currently page type'''
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    keywords = ['service','legal']
    with pytest.raises(ValueError):
        za_web.run(keywords,'blue')
    # NOTE: amrosnik chose not to write more unit tests for the run() function
    # because the tests would take too long to run. 
    # Future maintainers: consider writing proper integration tests utilizing run()
   
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
    za_web.teardown()

def test_get_pdfs(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    links = za_web.search_mandates('service',za_web.downloadPath)
    za_web.get_pdfs(links,path=za_web.downloadPath+"mandates/")
    assert len(os.listdir(za_web.downloadPath+'mandates/')) == 3
    shutil.rmtree(za_web.downloadPath+"mandates/")
    shutil.rmtree(za_web.downloadPath)
    za_web.teardown()

def test_run_constit(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    keywords = ['service','legal']
    matches = za_web.run_constitution(keywords)
    expected = ['constit/Act_200_of_1993_Constitution_of_the_Republic_of_South_Africa_Act_Interim_Constitution.pdf','constit/Act_34_of_2001_Constitution_of_the_Republic_of_South_Africa_Amendment_Act.pdf','constit/Act_3_of_2003_Constitution_of_the_Republic_of_South_Africa_Second_Amendment_Act.pdf','constit/SAConstitution.pdf']
    matches = [ m.replace(za_web.downloadPath,"") for m in matches ] 
    matches.sort()
    expected.sort()
    assert len(matches) == 4
    assert matches == expected
    shutil.rmtree(za_web.downloadPath+"constit/")
    shutil.rmtree(za_web.downloadPath)
    za_web.teardown()
  
def test_run_mandates(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    keywords = ['service','legal']
    matches = za_web.run_mandates(keywords)
    za_web.teardown()
    expected = ['mandates/329848_1.pdf','mandates/568169_1.pdf','mandates/568170_1.pdf','mandates/568171_1.pdf','mandates/568173_1.pdf','mandates/568473_1.pdf']
    matches = [ m.replace(za_web.downloadPath,"") for m in matches ] 
    matches.sort()
    expected.sort()
    assert len(matches) == 6
    assert matches == expected
    shutil.rmtree(za_web.downloadPath+"mandates/")
    shutil.rmtree(za_web.downloadPath)
