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
from legiscrapor import selsearch
import re
from legiscrapor import nlpIE
from legiscrapor import pdf_saver as ps 

#### ######## ######## ######## ########
#### This is the generic class used to 
#### define basic functions for web-crawling 
#### on a legislation website.
#### All specific country classes will, 
#### eventually, inherit from this class. 
#### ######## ######## ######## ########

class legisWeb():

  def __init__(self, driverLocation,downloadPath,options):
    ## setting up the class. The most important bit is to initialize the chromedriver 
    ## using a local driver location and various options. 
    ## options help ensure PDFs are downloaded correctly and in the correct location.
    ## passing downloadPath here, too, for ease of use later for downloading PDFs into specific subdirs
    self.driver = webdriver.Chrome(driverLocation,options=options)
    self.downloadPath = downloadPath
    self.country = "GENERIC"
    self.language = "English" ## the default language is English 
    self.mincount = 1 ## the default number of keyword occurrences that must occur in a document. 

  def change_mincount(self,new_mincount):
      ## if one is trying to run the generic legisWeb code on a new mincount, 
      ## maybe they'll want to change the mincount attribute at some point...
      self.mincount = new_mincount

  def change_country(self,new_country):
      ## if one is trying to run the generic legisWeb code on a new country, 
      ## maybe they'll want to change the country attribute at some point...
      self.country = new_country

  def change_language(self,new_lang):
      ## if one is trying to run the generic legisWeb code on a new language, 
      ## maybe they'll want to change the language attribute at some point...
      self.language = new_lang

  def checkers(self):
      print("You have initialized an automated search of ",self.country," 's legislation and will download files to ",self.downloadPath)
  
  def teardown(self):
    ## how we quit Chromedriver when we are finished 
    self.driver.quit()
  
  def search_laws(self,website,keyword):
    ## initialize on a given website -- WHICH MUST INCLUDE HTTP 
    ## and start searching for a law section of the website
    ## and, from there, look for keywords specific to the legislation topic

    self.driver.get(website) 
    self.driver.set_window_size(1324, 752) # widen screen for ease of viewing

    ## given our language, let's see if any legislation-y words are present in the dropdown menu. 
    ## pretty much every website has a dropdown menu.

    ## IMPORTANT NOTE: This method in the parent class legisWeb will NOT get actual hrefs. 
    ## it is merely a blueprint for how to look for relevant search terms. 
    ## Pretty much every website has a unique way of coding HTML tags for dropdown menus, so 
    ## This will serve as a way to tell you where legislative documents are most likely to be found.
    ## Consequently, if one wants to actually download PDFs for a random legislation website, 
    ## one will need to either create custom code for that country, or do it manually. :( 
    dropdowns = self.get_dropdown_words() 
    success = 0
    dropdown_prospects = dict()
    if len(dropdowns) > 0 :
        for d in dropdowns:
           #while success == 0: 
              elements = self.driver.find_elements_by_partial_link_text(d)
              dropdown_prospects[d] = len(elements)
              #if len(elements) > 0: 
              #    for el in elements:
              #        el.click()
              #success = success + 1 

    print("Here are the words most likely to be in relevant dropdown link names for this legislative website:")
    for d in dropdown_prospects.keys():
        if dropdown_prospects[d] > 0:
           print(d) 

    hrefs = []
    search_results = []
    
    ## store all of the link strings in a list
    if len(search_results) > 0:
       hrefs = [s.get_attribute('href') for s in search_results]
       hrefs = list(set(hrefs)) # get only unique links
    return(hrefs) 

  def get_pdfs(self,links,path=os.getcwd(),anotherLink=False):
    ## given a list of links, click all of them to automatically download their associated PDFs. 
    source_dir = self.downloadPath
    target_dir = path
    if source_dir != target_dir:
       if not os.path.exists(target_dir):
          os.makedirs(target_dir)

    if len(links) > 0:
        for link in links: 
               self.driver.get(link) # when this link is clicked, the PDF will be downloaded automatically
               self.driver.implicitly_wait(10)

               if anotherLink:
                  ## in case the links in links go to HTML pages/versions of legislation with hyperlinks therein for PDF downloads
                  ## so far, only Kenya behaves this way.
                  ## the relative xpath shown here is what's there for Kenya, and it probably differs for other websites.  
                  pdf_link = self.driver.find_element_by_xpath('//td[@style="width: 20px;"]/a[@target="_blank"]')
                  pdf_link = pdf_link.get_attribute('href')
                  self.driver.get(pdf_link)
               
               time.sleep(2)

    time.sleep(40)
    file_names = []
    for fname in os.listdir(source_dir):
       pathy = os.path.join(source_dir, fname)
       if os.path.isdir(pathy):
           # skip directories
           continue
       else:
           file_names.append(fname)

    if source_dir != target_dir:
       for file_name in file_names:
          dest = os.path.join(target_dir,file_name)
          if not os.path.isfile(dest):
             shutil.move(os.path.join(source_dir, file_name), target_dir)

  def scan_pdfs(self,download_path,keywords):
    df = ps.scan_pdfs(download_path)

    matches = nlpIE.full_nlp_ie(df,keywords,self.language,self.mincount)
    return(matches)

  def search_for_words(self,link,keywords):
    self.driver.get(link)
    whole_page = self.driver.page_source
    counts = selsearch.search_for_keywords(whole_page,keywords,min_count=self.mincount)
    return(counts)
 
  def find_links_by_pattern(self,tags,pattern,keywords): 
    n_elements = self.driver.find_elements_by_xpath(tags)
    matches = selsearch.find_keywords_from_links(self.driver,n_elements,pattern,keywords,waittime=5,min_count=self.mincount)
    return(matches)

  def print_matches(self,matches,specs,path=os.getcwd()): 
      ## method for printing a matches list, which is a list of file names that had relevant keywords found in them
      mfile = open(path+'/matches_'+specs+'.txt', 'w')

      for m in matches:
         mfile.write(m)
         mfile.write('\n')
         mfile.write(' \n')
      mfile.close()

  def delete_unneeded_files(self,specs,exceptions,files_path='',path=os.getcwd()):
    ## delete files not deemed likely candidates by scan_pdfs(), 
    ## but save a plain text file of the file names in case someone is curious. 
    mfile = open(path+'/deleted-files_'+specs+'.txt', 'w')
    if files_path == '':
        files_path = self.downloadPath

    for fname in os.listdir(files_path):
       pathy = os.path.join(files_path, fname)
       if pathy in exceptions and len(exceptions) > 0:
           # *exceptions* is a list of files to exclude from this deletion process
           continue
       elif os.path.isdir(pathy):
           # skip directories
           continue
       else:
           if os.path.isfile(pathy):
               #print("Now deleting..."+pathy)
               mfile.write(pathy)
               mfile.write('\n')
               mfile.write(' \n')
               os.remove(pathy)
    mfile.close()

  def get_dropdown_words(self):
      dropdown_words = {'English': ['Law','law','Parliament','parliament','Congress','congress','Legislation','legislation','Legislature','legislature','Document','document','Legal','legal']}
      words = []
      try: 
          words = dropdown_words.get(self.language)
      except:
          print("ERROR: The language "+self.language+" is currently not supported.")
     
      return(words)

  def delete_no_matches(self,specs,path=os.getcwd()): 
      ## let's delete any files not saved in the matches plain text file:
      match_exceptions = [] 
      with open(os.path.join(os.getcwd(), 'matches_'+specs+'.txt'), 'r') as f:
         lines = f.readlines()
         for line in lines:
            if len(line) > 2: # blank-ish \n lines apparently have len=2 based on how I wrote this.
               line = line.split('\n')[0]
               match_exceptions.append(line)
      self.delete_unneeded_files('no-NLP-match_'+specs,match_exceptions,files_path=path)
      #self.delete_unneeded_files('no-NLP-match_'+specs,match_exceptions,files_path=self.downloadPath)



