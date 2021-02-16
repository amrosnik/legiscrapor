"""
Test for searching South Africa Parliament website for legal aid content.

The class legisSouthAfrica was originally generated by Selenium IDE.
However, it has been converted to a Chromedriver for ease of use,
and added lots of custom functionality.
"""

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import re
import os
import datetime
import shutil 
import numpy as np 
from legiscrapor import nlpIE
from legiscrapor import pdf_saver as ps 
from legiscrapor.legisweb_class import legisWeb 
from legiscrapor import selsearch


class legisSouthAfrica(legisWeb):
  def __init__(self, driverLocation, downloadPath, options):
      super().__init__(driverLocation, downloadPath, options)
      self.country = "South Africa"

  def search_legislation(self,sublink_text):
    ## generic function for finding a specific element in the Legislation dropdown menu.
    ## the driver commands were generated with the Selenium IDE in firefox.
    self.driver.get("https://www.parliament.gov.za/")
    self.driver.set_window_size(1324, 752) # make the window bigger for ease of viewing 
    self.driver.find_element(By.CSS_SELECTOR, ".mega-menu:nth-child(4) > a").click()
    self.driver.implicitly_wait(5)
    self.driver.find_element(By.LINK_TEXT, "Legislation").click()
    self.driver.implicitly_wait(5)
    final_link = self.driver.find_element(By.LINK_TEXT, sublink_text)
    final_href = final_link.get_attribute('href')
    final_link.click()

    self.driver.implicitly_wait(5)
    self.driver.get(final_href)

    return(final_href)

  def search_mandates(self,keyword,download_path):
    ## function for obtaining lots of links for searching the Mandates database for a specific keyword. 
    ## the driver commands were generated with the Selenium IDE in firefox.
    base = "https://www.parliament.gov.za"

    self.driver.get(base+"/mandates?queries[search]="+keyword+"&sorts[date]=-1&perPage=50") # we use this link to avoid interacting with the dynamic table
    ## perPage = 50 indicates 50 table results/page view 
    self.driver.set_window_size(1324, 752)
    self.driver.implicitly_wait(5)

    trs = self.driver.find_elements_by_xpath('//tbody/tr[@style="cursor:pointer"]')
    extracted_links = [link.get_attribute("onclick").strip("window.open(").strip("','_blank')") for link in trs]
    table_length = len(extracted_links)
    #print(keyword,table_length)

    links = []
    if table_length > 0:
        ## search for data-dynatable-page selectors.
        for i in range(1,35): # for the Mandates page, there are 34 total pages. 
            ## I'm keeping this loop structure for now in case I figure out an intelligent way 
            ## to get the dynamic table results for any page beyond page 1. 
            page_found = True
            try:
                page_found = True
                self.driver.find_element(By.LINK_TEXT, str(i)).click()
                self.driver.implicitly_wait(5)
                trs_page = self.driver.find_elements_by_xpath('//tbody/tr[@style="cursor:pointer"]')
                links = [link.get_attribute("onclick").strip("window.open(").strip("','_blank')") for link in trs_page]
                #print(links)
            except:
                if i == 2: 
                    print("more than 50 results found. We will consider anything beyond 50 results negligible. Results are given in terms of chronological order, with newest legislation first.") 
                page_found = False
                if i > 2: 
                    break

    return(links)

  def get_pdfs(self, links, useBase=True, path=os.getcwd()):
    """
    Given a list of links, click all of them to automatically
    download their associated PDFs.
    """
    base = "https://www.parliament.gov.za"
    if len(links) > 0:
        for link in links: 
            if useBase:
               self.driver.get(base+link) # when this link is clicked, the PDF will be downloaded automatically
            else:
               self.driver.get(link) # when this link is clicked, the PDF will be downloaded automatically
    ## move resulting PDFs to the custom path. This helps keep self.downloadPath clean
    time.sleep(40)
    source_dir = self.downloadPath
    target_dir = path
    if source_dir != target_dir:
       if not os.path.exists(target_dir):
          os.makedirs(target_dir)

    file_names = []
    for fname in os.listdir(source_dir):
       pathy = os.path.join(source_dir, fname)
       if os.path.isdir(pathy):
           # skip directories
           continue
       if 'CONSTITUTION_COMIC_eng' in pathy:
           continue # this document doesn't get read correctly by PDF readers
       else:
           file_names.append(fname)

    if source_dir != target_dir:
       for file_name in file_names:
          dest = os.path.join(target_dir,file_name)
          if not os.path.isfile(dest):
             shutil.move(os.path.join(source_dir, file_name), target_dir)

  def search_acts(self,word,year):
    base = "https://www.parliament.gov.za"
    self.driver.set_window_size(1324, 752)
    self.driver.get(base+"/acts?sorts[date]=-1&perPage=50&queries[search]="+word)
    self.driver.implicitly_wait(5)

    self.driver.find_element(By.ID, "docfilter").click()
    dropdown = self.driver.find_element(By.ID, "docfilter")
    #print(year,word)
    dropdown.find_element(By.XPATH, "//option[. = "+str(year)+"]").click()

    self.driver.implicitly_wait(10)
    trs = self.driver.find_elements_by_xpath('//tbody/tr/td[@style="text-align: left;"]/a')
    extracted_links = [link.get_attribute('href') for link in trs]
    #table_length = len(extracted_links)
    #print(word,table_length)
    return(extracted_links)

  def run_constitution(self,keywords):
    ## the overall process for searching The Constitution main page for keywords.
    download_path = self.downloadPath+"/constit/"
    constit = self.search_legislation("The Constitution") # get to the Constitution page

    counts = self.search_for_words(constit,keywords) # search the Constitution landing page for keywords

    ## get all PDF links
    tags = '//a[starts-with(@href,"/storage/app/media")]'
    trs = self.driver.find_elements_by_xpath(tags)
    extracted_links = [link.get_attribute('href') for link in trs]

    match_files = []
    ## download + analyze all PDFs 
    if len(extracted_links) > 0:
       self.get_pdfs(extracted_links,useBase=False,path=download_path)
       match_files = self.scan_pdfs(download_path,keywords)
    return(match_files)

  def run_mandates(self,keywords): 
    ## the overall process for searching The Mandates main page for keywords.
    download_path = self.downloadPath+"/mandates/"
    all_match_files = []
    for word in keywords:
       links = self.search_mandates(word,download_path) # for each keyword, run a dynamic table search + save all relevant PDFs
       #print(links)
       if len(links) > 0:
          self.get_pdfs(links,path=download_path)
          match_files = self.scan_pdfs(download_path,keywords) # analyze PDF results
          if len(match_files) > 0:
              all_match_files.append(match_files)

    all_match_files = [item for sublist in all_match_files for item in sublist]
    all_match_files = np.unique(all_match_files)

    return(all_match_files)

  def run_acts(self,keywords): 
    ## the overall process for searching The Acts main page for keywords.
    download_path = self.downloadPath+"/acts/"
    all_links = []
    match_files = []
    for word in keywords:
      for y in range(1994,2005): # The Acts dynamic table is filtered by YEAR and KEYWORD. Hence the double loop.
      #for y in range(1994,int(datetime.datetime.now().year)+1): # The Acts dynamic table is filtered by YEAR and KEYWORD. Hence the double loop.
          links = self.search_acts(word,y) # for each keyword + year combo, run dynamic table search
          links = list(set(links))
          #print(y,word)
          #print("****** LINKS ******")
          #print(links)
          all_links = np.append(all_links,links)
          #print("****** ALL_LINKS ******")
          #print(all_links)
          self.driver.implicitly_wait(60)
          #time.sleep(5)
      #print(all_links)
    for word in keywords:
      for y in range(2005,2020): # The Acts dynamic table is filtered by YEAR and KEYWORD. Hence the double loop.
      #for y in range(1994,int(datetime.datetime.now().year)+1): # The Acts dynamic table is filtered by YEAR and KEYWORD. Hence the double loop.
          links = self.search_acts(word,y) # for each keyword + year combo, run dynamic table search
          links = list(set(links))
          #print(y,word)
          #print("****** LINKS ******")
          #print(links)
          all_links = np.append(all_links,links)
          #print("****** ALL_LINKS ******")
          #print(all_links)
          self.driver.implicitly_wait(60)
          #time.sleep(5)
      #print(all_links)
    # TODO: create dict for word:all_of_the_links ???
    all_links = np.unique(all_links)
    #print(all_links)

    ## download + analyze all PDFs 
    self.get_pdfs(all_links,useBase=False,path=download_path)
    match_files = self.scan_pdfs(download_path,keywords)  
    return(match_files)

  def run_bills(self,keywords): 
    other_bills = self.search_legislation("Other Bills")

    ## scrape resulting page for specific text. Print the results. 
    #keywords = ["bill","House"] 
    counts = self.search_for_words(other_bills,keywords)
    #print(counts)

    ## click a link + search resulting page for links w/ certain words in xpath/link text. 
    ## then click on all links found and search for keyword matches. 
    pattern = re.compile(r'')
    tags = '//a'
    matches = self.find_links_by_pattern(tags,pattern,keywords)
    #print(matches)
    # TODO: WARNING: This is broken. It is unreasonable to search literally ALL the links on the Other Bills page.
    # Do Bills, in the context of South Africa, matter? Bills aren't laws yet. Do we only care about actual, in-place laws?  

  def run(self,keywords,page_type): 
      webpage_help = """
      Select from:
      1=Constitution
      2=Mandates
      3=Acts
      4=Other Bills
      """
      if page_type == 'constit':
          matches = new_za.run_constitution(keywords)
      elif page_type = 'mandates':
          matches = new_za.run_mandates(keywords)
      elif page_type = 'acts':
          matches = new_za.run_acts(keywords) 
      elif page_type = 'bills':
          matches = new_za.run_bills(keywords)
      else: 
          error_msg = 'ERROR: webpage integer indicator not found.'
          raise ValueError(error_msg + webpage_help)


