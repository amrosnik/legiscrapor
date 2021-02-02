import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import argparse
import pandas as pd
import numpy as np 
import os
import shutil 
import selsearch
import re
import nlpIE
import pdf_saver as ps 
from legisweb_class import legisWeb

class legisKenya(legisWeb):

  def __init__(self, driverLocation,downloadPath,options):
      super().__init__(driverLocation,downloadPath,options)
      self.country = "Kenya" 

  def search_laws(self,website,keyword):
    ## This function overwrites legisWeb.search_laws() 
    ## since we know specifically how Kenya's website works. 

    self.driver.get(website) 
    self.driver.set_window_size(1324, 752)
    self.driver.find_element(By.LINK_TEXT, "Laws of Kenya").click() 
    self.driver.find_element(By.CSS_SELECTOR, "li:nth-child(3) em").click()
    self.driver.find_element(By.ID, "txtFTSearch").click()
    self.driver.find_element(By.ID, "txtFTSearch").send_keys(keyword)
    self.driver.find_element(By.ID, "btnFTSearch").click()
    self.driver.implicitly_wait(50)
    search_results = self.driver.find_elements_by_xpath('//div[@id="results-grid"]/div[@class="act search-result"]/div[@class="act-title"]/a')
    hrefs = [s.get_attribute('href') for s in search_results]
    hrefs = list(set(hrefs)) # get only unique links
    return(hrefs) 

