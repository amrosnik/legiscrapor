from selenium import webdriver
import re
from legiscrapor import selsearch
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import pytest
from legiscrapor.legisweb_class import legisWeb 
import os 
import shutil

#### UNIT TESTS FOR SELSEARCH MODULE ####

## VERY IMPORTANT: please modify the customize_me.txt file 
## in the data/ folder before running these tests! 
## follow instructions in the file to ensure your chromedriver can be located correctly. 

@pytest.fixture
def lw():
    '''Returns a LegisWeb instance with English as the language, 
    input args as described in customize_me.txt '''
    lw = legisWeb()
    lw.read_inputs("./src/legiscrapor/data/customize_me.txt",notTesting=False)
    return(lw) 

@pytest.fixture
def whole_page():
    ''' Returns the HTML source code for a webpage on the India Legislative website, 
    https://legislative.gov.in/about-us/about-departments '''
    with open('./src/legiscrapor/data/legislative-dot-gov-dot-in__about-us__about-departments.html', 'r') as f:
        webpage = f.read()
    return webpage

def test_find_keywords(whole_page):
    ''' test for keywords that actually appear on the whole_page webpage '''
    keywords = ["department", "ministry"]  
    counts = selsearch.search_for_keywords(whole_page, keywords)
    assert counts['department'] == 3
    assert counts['ministry'] == 2
    assert counts['TOTAL'] == 5

def test_no_keywords(whole_page): 
    ''' test for keywords that do NOT appear on the whole_page webpage '''
    keywords = ["blue","cake"]  
    counts = selsearch.search_for_keywords(whole_page, keywords)
    assert counts['blue'] == 0
    assert counts['cake'] == 0
    assert counts['TOTAL'] == 0

def test_keywords_from_links(lw):
    lw.init_driver()
    dr = lw.get_driver()
    dr.get('https://legislative.gov.in/about-us/about-departments')
    ne = dr.find_elements_by_xpath('//a')
    pattern = re.compile(r'Vision') # there should only be one link that matches this pattern in its link text / hyperlink name
    keywords = ['about'] 
    matches = selsearch.find_keywords_from_links(dr,ne,pattern,keywords)
    lw.teardown()
    assert len(matches) == 1 
    assert matches.loc[0,"href"] == 'https://legislative.gov.in/about-us/vision-mission-and-objectives'
    assert matches.loc[0,"keyword_matches"] == {'about': 10, 'TOTAL': 10} # the word 'about' appears 10 times in the source code of the Vision page

def test_no_pattern_keywords_from_links(lw):
    # unit test to ensure appropriate behavior for no pattern match 
    lw.init_driver()
    dr = lw.get_driver()
    dr.get('https://legislative.gov.in/about-us/about-departments')
    ne = dr.find_elements_by_xpath('//a')
    pattern = re.compile(r'blue') 
    keywords = ['about'] 
    matches = selsearch.find_keywords_from_links(dr,ne,pattern,keywords)
    lw.teardown()
    assert len(matches) == 0

def test_no_keywords_from_links(lw):
    # unit test to ensure appropriate behavior for pattern match but no keyword match 
    lw.init_driver()
    dr = lw.get_driver()
    dr.get('https://legislative.gov.in/about-us/about-departments')
    ne = dr.find_elements_by_xpath('//a')
    pattern = re.compile(r'Vision') 
    keywords = ['blue'] 
    matches = selsearch.find_keywords_from_links(dr,ne,pattern,keywords)
    lw.teardown()
    assert len(matches) == 1 
    assert matches.loc[0,"href"] == 'https://legislative.gov.in/about-us/vision-mission-and-objectives'
    assert matches.loc[0,"keyword_matches"] == {'blue': 0, 'TOTAL': 0} # the word 'blue' appears 0 times in the source code of the Vision page

