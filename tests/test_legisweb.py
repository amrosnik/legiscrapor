import pytest 
from legiscrapor.legisweb_class import legisWeb 
import os 
import shutil

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

#def test_search_laws(eng_web):

