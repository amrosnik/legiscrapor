from selenium import webdriver
import re 
from legiscrapor import selsearch
import pandas as pd 
from webdriver_manager.chrome import ChromeDriverManager
## test-driving Selenium on my own website.

# dataframe display settings
pd.set_option('display.max_row', 1050)
pd.set_option('display.max_column', 16)

## driver setup + select website of interest
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.maximize_window()
driver.get('https://andreanarosnik.com')

## BASIC TEST: click a link
code_link = driver.find_element_by_xpath(u'//a[text()="code"]')
code_link.click()
code_href = code_link.get_attribute('href')
driver.get(code_href)

## next: scrape resulting page for specific text. Print the results. 
whole_about_page = driver.page_source
keywords = ["absurd","silly", "surreal"] # none of these are on the page; total = 0 
keywords = ["R ","San Francisco", "data "] # all 3 of these appear on the page source code; totals = 3,4,3, total total=10

counts = selsearch.search_for_keywords(whole_about_page,keywords)
print(counts)

## SECOND TEST: click a link + search resulting page for links w/ certain words in xpath/link text. 
## then click on all links found and search for keyword matches. 

## let's look for all the links that start with a capital "N" 
pattern = re.compile(r'^N')

## find all anchor tags
#n_links = driver.find_elements_by_xpath('//a[contains(text(),"N")]')
n_elements = driver.find_elements_by_xpath('//a')

## find the keyword matches 
matches = selsearch.find_keywords_from_links(driver,n_elements,pattern,keywords)


driver.close()
       

