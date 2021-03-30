import pytest 
from legiscrapor.legissouthafrica import legisSouthAfrica
import os 
import shutil

#### UNIT TESTS FOR LEGISSOUTHAFRICA CLASS ####
## The following are unit tests 
## for the LegisSouthAfrica methods.
## The test name roughly corresponds with 
## the method it tests.
## As noted in other unit test files, 
## please customize the customize_me.txt file
## prior to running these tests 
## to ensure they actually work.

@pytest.fixture
def za_web():
    '''Returns a LegisSouthAfrica instance'''
    return legisSouthAfrica()

def test_language(za_web):
    assert za_web.language == "English"

def test_country(za_web):
    assert za_web.country == "South Africa"

def test_search_acts(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    links = za_web.search_acts('legal',1995)
    expected = ['https://www.parliament.gov.za/storage/app/media/Acts/1995/Act_43_of_1995_Legal_Succession_to_the_South_African_Transport_Services_Amendment_Act.pdf', 'https://www.parliament.gov.za/storage/app/media/Acts/1995/Act_43_of_1995_Legal_Succession_to_the_South_African_Transport_Services_Amendment_Act.pdf', 'https://www.parliament.gov.za/storage/app/media/Acts/1995/Act_33_of_1995_Admission_of_Legal_Practitioners_Amendment_Act.pdf', 'https://www.parliament.gov.za/storage/app/media/Acts/1995/Act_33_of_1995_Admission_of_Legal_Practitioners_Amendment_Act.pdf', 'https://www.parliament.gov.za/storage/app/media/Acts/1995/Act_10_of_1995_Recognition_of_Foreign_Legal_Qualifications_and_Practice_Amendment_Act.pdf', 'https://www.parliament.gov.za/storage/app/media/Acts/1995/Act_10_of_1995_Recognition_of_Foreign_Legal_Qualifications_and_Practice_Amendment_Act.pdf']
    links.sort()
    expected.sort()
    assert len(links) == 6
    assert links == expected

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
    za_web.teardown()
    assert constit_href == "https://www.parliament.gov.za/constitutional-amendments"

def test_search_mandates(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    links = za_web.search_mandates('service',za_web.downloadPath) 
    za_web.teardown()
    links.sort()
    expected = ['/storage/app/media/Docs/fin_man/329848_1.pdf', '/storage/app/media/Docs/fin_man/329850_1.pdf', '/storage/app/media/Docs/fin_man/329851_1.pdf']
    expected.sort()
    assert len(links) == 3
    assert links == expected

def test_get_pdfs(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    links = za_web.search_mandates('service',za_web.downloadPath)
    za_web.get_pdfs(links,path=za_web.downloadPath+"mandates/")
    za_web.teardown()
    assert len(os.listdir(za_web.downloadPath+'mandates/')) == 3
    shutil.rmtree(za_web.downloadPath+"mandates/")
    shutil.rmtree(za_web.downloadPath)

def test_run_constit(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    keywords = ['service','legal']
    matches = za_web.run_constitution(keywords)
    za_web.teardown()
    expected = ['constit/Act_200_of_1993_Constitution_of_the_Republic_of_South_Africa_Act_Interim_Constitution.pdf','constit/Act_34_of_2001_Constitution_of_the_Republic_of_South_Africa_Amendment_Act.pdf','constit/Act_3_of_2003_Constitution_of_the_Republic_of_South_Africa_Second_Amendment_Act.pdf','constit/SAConstitution.pdf']
    matches = [ m.replace(za_web.downloadPath,"") for m in matches ] 
    matches.sort()
    expected.sort()
    assert len(matches) == 4
    assert matches == expected
    shutil.rmtree(za_web.downloadPath+"constit/")
    shutil.rmtree(za_web.downloadPath)
  
def test_run_mandates(za_web):
    za_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    za_web.country = "South Africa"
    keywords = ['service','legal']
    matches = za_web.run_mandates(keywords)
    expected = ['mandates/329848_1.pdf','mandates/568169_1.pdf','mandates/568170_1.pdf','mandates/568171_1.pdf','mandates/568173_1.pdf','mandates/568473_1.pdf']
    matches = [ m.replace(za_web.downloadPath,"") for m in matches ] 
    matches.sort()
    expected.sort()
    assert len(matches) == 6
    assert matches == expected
    za_web.teardown()
    shutil.rmtree(za_web.downloadPath+"mandates/")
    shutil.rmtree(za_web.downloadPath)


