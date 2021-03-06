# Generated by Selenium IDE
#import pytest
import time
#import json
from selenium import webdriver
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import argparse
import pandas as pd 

class TestIndiaactssearch():
  # TODO: inheritance from South Africa class
  def setup(self, driverLocation,downloadPath,options):
    ## setting up the class. The most important bit is to initialize the chromedriver 
    ## using a local driver location and various options. 
    ## options help ensure PDFs are downloaded correctly and in the correct location.
    ## passing downloadPath here, too, for ease of use later for downloading PDFs into specific subdirs
    self.driver = webdriver.Chrome(driverLocation,options=options)
    self.vars = {}
    self.downloadPath = downloadPath
  
  # TODO: inheritance from South Africa class
  def teardown(self):
    ## how we quit Chromedriver when we are finished 
    self.driver.quit()
  
  def search_india_code(self):
    self.driver.get("https://www.indiacode.nic.in/")
    self.driver.set_window_size(1324, 752)
    self.driver.find_element(By.NAME, "searchradio").click()
    self.driver.find_element(By.ID, "tequery").click()
    #self.driver.find_element(By.ID, "tequery").send_keys("legal aid")
    #self.driver.implicitly_wait(50)
    #self.driver.find_element(By.ID, "btngo").click()
    #self.driver.find_element(By.ID, "tequery").click()
    #self.driver.find_element(By.ID, "tequery").click()
    self.driver.find_element(By.ID, "tequery").send_keys("legal service")
    self.driver.implicitly_wait(50)
    self.driver.find_element(By.CSS_SELECTOR, ".btn:nth-child(1)").click()
    """
    self.driver.find_element(By.LINK_TEXT, "The Legal Services Authorities Act, 1987").click()
    self.driver.find_element(By.CSS_SELECTOR, ".standard img").click()
    self.driver.find_element(By.LINK_TEXT, "The Supreme Court Legal Services Committee Rules, 2000").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col-sm-1 img").click()
    self.driver.find_element(By.LINK_TEXT, "THE NATIONAL LEGAL SERVICES AUTHORITY etLEGAL SERVICES CLINICS) REGULATIONS, 2011").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col-sm-1 img").click()
    self.driver.find_element(By.LINK_TEXT, "Authorize the State Authority and District Authority constituted under the Legal Services Authorities Act, 1987 for the purpose of pre-institution mediation and settlement under the Commercial Courts Act, 2015").click()
    self.driver.find_element(By.CSS_SELECTOR, ".col-sm-1 img").click()
    """

  def search_president_constit(self):
    self.driver.get("http://legislative.gov.in/")
    self.driver.set_window_size(1324, 752)
    self.driver.find_element(By.LINK_TEXT, "Read more").click()
    self.driver.find_element(By.LINK_TEXT, "Download (34.7 MB)").click()
    #self.driver.find_element(By.LINK_TEXT, "Download (93.89 MB)").click()
    #self.driver.find_element(By.LINK_TEXT, "Download (59.08 MB)").click()
    #self.driver.find_element(By.LINK_TEXT, "Download (69.29 MB)").click()
    #self.driver.find_element(By.LINK_TEXT, "Download (219.83 KB)").click()
    #self.driver.find_element(By.LINK_TEXT, "Download (40.67 MB)").click()
    #self.driver.find_element(By.LINK_TEXT, "Download (11.55 MB)").click()
    #self.driver.find_element(By.LINK_TEXT, "Download (31.47 MB)").click()




####### LET'S RUN THIS ####### 

## ARGPARSE: args for this script. 
parser = argparse.ArgumentParser(description='Extract PDFs of legislation from South African Parliament website.')
#parser.add_argument('webpage', metavar='webpage', type=int, 
#                    help='webpage to process. 1=Constitution,2=Mandates,3=Acts,4=Other Bills')
parser.add_argument('driver',help='Path for Chromedriver')
parser.add_argument('-path',help='Path for PDF downloads')

args = parser.parse_args()
download_path = str(args.path)

## setting up options for Chromedriver, mostly to ensure any PDF links automatically download the PDFs to download_path
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
"download.default_directory": download_path, #Change default directory for downloads
"download.prompt_for_download": False, #To auto download the file
"download.directory_upgrade": True,
"plugins.always_open_pdf_externally": True #It will not show PDF directly in chrome
})

new_india = TestIndiaactssearch() 
new_india.setup(args.driver,download_path,options)

pd.options.display.max_colwidth = 1000
#keywords =[ 'judicial assistance']
keywords = ['legal aid',
           'legal assistance']
#keywords = ['legal aid',
#           'legal assistance',
#           'legal service',
#           'judicial assistance']

#new_india.search_india_code()
new_india.search_president_constit()
