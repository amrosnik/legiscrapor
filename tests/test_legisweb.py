import pytest 
from legiscrapor.legisweb_class import legisWeb 
import os 
import shutil
import numpy as np 
import re 
import pandas as pd 

#### UNIT TESTS FOR LEGISWEB CLASS ####

## VERY IMPORTANT: please modify the customize_me.txt file 
## in the data/ folder before running these tests! 
## follow instructions in the file to ensure your chromedriver can be located correctly. 

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
    assert eng_web.downloadPath == "./src/legiscrapor/data/pdfsaver_docs/"
    assert eng_web.website == "http://kenyalaw.org/kl/"
    assert eng_web.language == "English"
    assert eng_web.keywords == ["legal aid", "judicial assistance", "legal assistance", "legal service"]
    assert eng_web.webpage == 1

def test_scan_pdfs(eng_web):
    eng_web.read_inputs("./src/legiscrapor/data/testing_input.txt",notTesting=False)
    matches = eng_web.scan_pdfs('./src/legiscrapor/data/pdfsaver_docs/',eng_web.keywords)
    assert len(matches) ==  4

def test_print_matches(eng_web): 
    eng_web.read_inputs("./src/legiscrapor/data/testing_input.txt",notTesting=False)
    matches = eng_web.scan_pdfs('./src/legiscrapor/data/pdfsaver_docs/',eng_web.keywords)

    # write matches to file: 
    specs = 'TESTING'
    matches_file = os.path.join(eng_web.downloadPath,'matches_'+specs+'.txt') 
    eng_web.print_matches(matches,specs)

    assert os.path.isfile(matches_file)

    # check that matches_file contains the expected content:
    if os.path.exists(matches_file): 
        with open(matches_file,'r') as f:
            lines = f.readlines() 
            assert lines == ['./src/legiscrapor/data/pdfsaver_docs/Act_20_of_1996_Legal_Aid_Amendment_Act.pdf\n', ' \n', './src/legiscrapor/data/pdfsaver_docs/Bangladesh_2000_Legal_Aid_Services_Act_eng.pdf\n', ' \n', './src/legiscrapor/data/pdfsaver_docs/Ghana_2018_Legal_Aid_Commission_Act_eng_1.pdf\n', ' \n', './src/legiscrapor/data/pdfsaver_docs/Sweden_1997_Legal_Aid_Regulation_eng.pdf\n', ' \n']

def test_dropdown(eng_web):
    words = eng_web.get_dropdown_words()

    # since this is an English language legisWeb instance, we expect all the English results:
    assert words == ['Law','law','Parliament','parliament','Congress','congress','Legislation','legislation','Legislature','legislature','Document','document','Legal','legal']

def test_delete_unneeded_files(eng_web):
    eng_web.read_inputs("./src/legiscrapor/data/testing_input.txt",notTesting=False)
    matches = list(eng_web.scan_pdfs('./src/legiscrapor/data/pdfsaver_docs/',eng_web.keywords))

    specs = 'TESTING'

    eng_web.delete_unneeded_files(specs,matches,path=eng_web.downloadPath,moveNotDelete=True)

    assert os.path.isdir(eng_web.downloadPath+"no-NLP-match")
    assert len(os.listdir(eng_web.downloadPath+"no-NLP-match")) == 1 

    # check that moved-files_file contains the expected content:
    moved_file = os.path.join(eng_web.downloadPath,'moved-files_'+specs+'.txt') 
    if os.path.exists(moved_file): 
        with open(moved_file,'r') as f:
            lines = f.readlines() 
            assert lines == ['./src/legiscrapor/data/pdfsaver_docs/Pakistan_1999_Bar_Council_Free_Legal_Aid_Rules.doc\n', ' \n']

    # move .doc file back to pdfsaver_docs/, delete no-NLP-match dir, delete intermediate .txt's
    shutil.move(eng_web.downloadPath+'no-NLP-match/Pakistan_1999_Bar_Council_Free_Legal_Aid_Rules.doc',eng_web.downloadPath)
    shutil.rmtree(eng_web.downloadPath+"no-NLP-match")
    os.remove(moved_file)
    matches_file = os.path.join(eng_web.downloadPath,'matches_'+specs+'.txt') 
    os.remove(matches_file)


def test_delete_matches(eng_web):
    eng_web.read_inputs("./src/legiscrapor/data/testing_input.txt",notTesting=False)
    matches = eng_web.scan_pdfs('./src/legiscrapor/data/pdfsaver_docs/',eng_web.keywords)

    specs = 'TESTING'
    # this is basically a slightly different way to do the test_delete_unneeded_files() test...
    eng_web.print_matches(matches,specs)
    eng_web.delete_no_matches(specs,path=eng_web.downloadPath,moveFiles=True)

    assert os.path.isdir(eng_web.downloadPath+"no-NLP-match")
    assert len(os.listdir(eng_web.downloadPath+"no-NLP-match")) == 1 

    # check that moved-files_file contains the expected content:
    moved_file = os.path.join(eng_web.downloadPath,'moved-files_no-NLP-match_'+specs+'.txt') 
    if os.path.exists(moved_file): 
        with open(moved_file,'r') as f:
            lines = f.readlines() 
            assert lines == ['./src/legiscrapor/data/pdfsaver_docs/Pakistan_1999_Bar_Council_Free_Legal_Aid_Rules.doc\n', ' \n']

    # move .doc file back to pdfsaver_docs/, delete no-NLP-match dir, delete intermediate .txt's
    shutil.move(eng_web.downloadPath+'no-NLP-match/Pakistan_1999_Bar_Council_Free_Legal_Aid_Rules.doc',eng_web.downloadPath)
    shutil.rmtree(eng_web.downloadPath+"no-NLP-match")
    os.remove(moved_file)
    matches_file = os.path.join(eng_web.downloadPath,'matches_'+specs+'.txt') 
    os.remove(matches_file)

def test_init_driver(eng_web):
    eng_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    # basically, just need to see if this command works. 
    # if this test fails, then it fails to locate chromedriver 
    # and initialize a Selenium webdriver.
    eng_web.teardown()

def test_search_laws(eng_web,capfd):
    eng_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)

    k = 'judicial assistance'

    hrefs = eng_web.search_laws(k)
    out,err = capfd.readouterr()
    patterns = ['Law','Parliament','Legal']
    for p in patterns: 
        assert re.search(p,out)
    assert len(hrefs) == 0
    eng_web.teardown()
   
def test_search_for_words(eng_web):
    ''' test for keywords that actually appear on the whole_page webpage '''
    eng_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    keywords = ["department", "ministry"]
    link = 'https://legislative.gov.in/about-us/about-departments'
    counts = eng_web.search_for_words(link,keywords)
    eng_web.teardown()
    assert counts['department'] == 3
    assert counts['ministry'] == 2
    assert counts['TOTAL'] == 5

def test_search_for_no_words(eng_web):
    ''' test for keywords that do NOT appear on the whole_page webpage '''
    eng_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    keywords = ["blue","cake"]  
    link = 'https://legislative.gov.in/about-us/about-departments'
    counts = eng_web.search_for_words(link,keywords)
    eng_web.teardown()
    assert counts['blue'] == 0
    assert counts['cake'] == 0
    assert counts['TOTAL'] == 0

def test_keywords_from_links(eng_web):
    ''' test for keywords that appear on the webpage '''
    eng_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    eng_web.driver.get('https://legislative.gov.in/about-us/about-departments')
    pattern = re.compile(r'Vision') # there should only be one link that matches this pattern in its link text / hyperlink name
    keywords = ['about'] 
    matches = eng_web.find_links_by_pattern('//a',pattern,keywords)
    eng_web.teardown()
    assert len(matches) == 1 
    assert matches.loc[0,"href"] == 'https://legislative.gov.in/about-us/vision-mission-and-objectives'
    assert matches.loc[0,"keyword_matches"] == {'about': 10, 'TOTAL': 10} # the word 'about' appears 10 times in the source code of the Vision page

def test_no_pattern_keywords_from_links(eng_web):
    # unit test to ensure appropriate behavior for no pattern match 
    eng_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    eng_web.driver.get('https://legislative.gov.in/about-us/about-departments')
    pattern = re.compile(r'blue') # there should only be one link that matches this pattern in its link text / hyperlink name
    keywords = ['about'] 
    matches = eng_web.find_links_by_pattern('//a',pattern,keywords)
    eng_web.teardown()
    assert len(matches) == 0

def test_no_keywords_from_links(eng_web):
    # unit test to ensure appropriate behavior for pattern match but no keyword match 
    eng_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    eng_web.driver.get('https://legislative.gov.in/about-us/about-departments')
    pattern = re.compile(r'Vision') # there should only be one link that matches this pattern in its link text / hyperlink name
    keywords = ['blue'] 
    matches = eng_web.find_links_by_pattern('//a',pattern,keywords)
    eng_web.teardown()
    assert len(matches) == 1 
    assert matches.loc[0,"href"] == 'https://legislative.gov.in/about-us/vision-mission-and-objectives'
    assert matches.loc[0,"keyword_matches"] == {'blue': 0, 'TOTAL': 0} # the word 'blue' appears 0 times in the source code of the Vision page

def test_get_pdfs(eng_web):
    # test that PDFs download correctly.
    # note that this requires downloading PDFs to your computer -- 
    # PLEASE update downloadPath in customize_me.txt before running!! 
    links = ['http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=CAP.%20198','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=CAP.%20326','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2011%20of%202016','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2013%20of%202019','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2014%20of%202019','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2016%20of%202013','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2019%20of%202011','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%202%20of%202000','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%202%20of%202009','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2021%20of%202017','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2024%20of%202011','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2026%20of%202015','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2028%20of%202011','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%204%20of%202006','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%204%20of%202016','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2043%20of%202016','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%2047%20of%202013','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%206%20of%202012','http://kenyalaw.org:8181/exist/kenyalex/actview.xql?actid=No.%208%20of%201999']
    eng_web.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=True)
    eng_web.get_pdfs(links,path=eng_web.downloadPath+'kenya_pdfs/',anotherLink=True) 
    assert len(os.listdir(eng_web.downloadPath+'kenya_pdfs/')) == 19
    shutil.rmtree(eng_web.downloadPath+"kenya_pdfs")
    shutil.rmtree(eng_web.downloadPath)
    eng_web.teardown()
    

