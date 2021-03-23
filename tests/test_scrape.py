from selenium import webdriver
import re
from legiscrapor import selsearch
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import pytest

"""
# dataframe display settings
pd.set_option('display.max_row', 1050)
pd.set_option('display.max_column', 16)

# driver setup + select website of interest
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get('https://andreanarosnik.com')

# BASIC TEST: click a link
code_link = driver.find_element_by_xpath(u'//a[text()="code"]')
code_link.click()
code_href = code_link.get_attribute('href')
driver.get(code_href)

## next: scrape resulting page for specific text. Print the results.
whole_about_page = driver.page_source
"""

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

"""
# SECOND TEST: click a link + search resulting page for links w/ certain words in xpath/link text.
# then click on all links found and search for keyword matches.

# let's look for all the links that start with a capital "N"
pattern = re.compile(r'^N')

# find all anchor tags
# n_links = driver.find_elements_by_xpath('//a[contains(text(),"N")]')
n_elements = driver.find_elements_by_xpath('//a')

# find the keyword matches
matches = selsearch.find_keywords_from_links(driver, n_elements, pattern, keywords)

driver.close()
"""
