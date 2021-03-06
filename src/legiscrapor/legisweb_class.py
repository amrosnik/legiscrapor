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
import glob 

#### ######## ######## ######## ########
#### This is the generic class used to 
#### define basic functions for web-crawling 
#### on a legislation website.
#### All specific country classes will, 
#### eventually, inherit from this class. 
#### ######## ######## ######## ########

class legisWeb():

  def __init__(self):
      self.country = "GENERIC"
      self.language = "English" ## the default language is English 
      self.mincount = 1 ## the default number of keyword occurrences that must occur in a document. 
  
  def read_inputs(self,inputFile,notTesting=True):
      ## setting up the class based on data from inputFile, which is a plain text file. 
      ## The most important bit is to initialize the chromedriver 
      ## using a local driver location and various options...but this will be done in another function. 
      ## here we merely grab the strings needed to do so later.
      
      ## notTesting is a boolean value to distinguish if we are in a testing mode (notTesting = False) 
      ## or not (the default value, notTesting = True) 
      self.inputs = []
      with open(inputFile, "r") as f:
          lines = f.readlines()
      for i in range(0, len(lines)):
          if lines[i][0] == "#" or lines[i][0] == '\n':
              continue
          self.inputs.append(lines[i])
      # 1st argument: Parse the chromedriver location; will set this up in init_driver()
      self.inputs[0] = self.inputs[0].strip(" \n") 
      # 2nd argument: downloadPath
      self.downloadPath = self.inputs[1].strip(" \n")
      if notTesting and not os.path.exists(self.downloadPath):
          os.makedirs(self.downloadPath)
      # 3rd argument: main website
      self.website = self.inputs[2].strip(" \n")
      # 4th argument: country
      self.country = self.inputs[3].strip(" \n")
      # 5th argument: language
      self.language = self.inputs[4].strip(" \n")
      # 6th argument: keywords for this class instance 
      self.keywords = self.inputs[5].split(",")
      self.keywords = [k.strip(" \n") for k in self.keywords]
      # 7th argument: webpage 
      # (used for South Africa and similar websites that have legislation on different parts of the website)
      self.webpage = int(self.inputs[6].strip(" \n"))
  
      if notTesting:
         self.init_driver()
 
  def init_driver(self):
      ## set up the Chromedriver. 
      ## options help ensure PDFs are downloaded correctly and in the correct location.
      ## passing downloadPath here, too, for ease of use later for downloading PDFs into specific subdirs

      ## setting up options for Chromedriver, 
      ## mostly to ensure any PDF links automatically download the PDFs to download_path
      options = webdriver.ChromeOptions()
      options.add_experimental_option('prefs', {
      "download.default_directory": self.downloadPath, #Change default directory for downloads
      "download.prompt_for_download": False, #To auto download the file
      "download.directory_upgrade": True,
      "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome
      "safebrowsing.enabled": True # try safe-browsing to ensure this works on Windows 
      })

      self.driver = webdriver.Chrome(self.inputs[0],options=options)

  def get_driver(self):
      # returns the chromedriver in case it needs to get passed along externally...
      return(self.driver)

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
  
  def search_laws(self,keyword):
      ## initialize on a given website (the website saved as a class attribute)-- WHICH MUST INCLUDE HTTP 
      ## and start searching for a law section of the website
      ## and, from there, look for keywords specific to the legislation topic
     
      self.driver.get(self.website) 
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

  def print_matches(self,matches,specs): 
      ## method for printing a matches list, which is a list of file names that had relevant keywords found in them
      mfile = open(os.path.join(self.downloadPath,'matches_'+specs+'.txt'), 'w')

      for m in matches:
         mfile.write(m)
         mfile.write('\n')
         mfile.write(' \n')
      mfile.close()


  def delete_unneeded_files(self,specs,exceptions,files_path='',path=os.getcwd(),moveNotDelete=False):
      ## delete files not deemed likely candidates by scan_pdfs(), 
      ## but save a plain text file of the file names in case someone is curious. 
      ## if moveNotDelete is True, then the files get moved to a new dir instead of deleted. 
      if moveNotDelete:
         dfile = os.path.join(self.downloadPath,'moved-files_'+specs+'.txt')
      else:
         dfile = os.path.join(self.downloadPath,'deleted-files_'+specs+'.txt')
      mfile = open(dfile, 'w')
      if files_path == '':
          files_path = self.downloadPath
   
      ## add these to exceptions just in case path = self.downloadPath
      all_excepts = []
      bfiles = glob.glob(os.path.join(self.downloadPath,'matches_*.txt'))
      for b in bfiles:
         all_excepts.append(b)
      nfiles = glob.glob(os.path.join(self.downloadPath,'deleted-files_*.txt'))
      for n in nfiles:
         all_excepts.append(n)
      mfiles = glob.glob(os.path.join(self.downloadPath,'moved-files_*.txt'))
      for m in mfiles:
         all_excepts.append(m)
      lfiles = glob.glob(os.path.join(self.downloadPath,'low_*.txt'))
      for l in lfiles:
         all_excepts.append(l)
      print(all_excepts)
      for a in all_excepts:
         if os.path.isfile(a):
            exceptions.append(a)

      if os.path.isdir(files_path):
         for fname in os.listdir(files_path):
            pathy = os.path.join(files_path, fname)
            if pathy in exceptions and len(exceptions) > 0:
                # *exceptions* is a list of files to exclude from this deletion process
                continue
            elif os.path.isdir(pathy):
                if "temp_images" in pathy:
                    # remove the temp_images/ dir created by pdf_saver 
                    # when a PDF needs to be converted to multiple image files 
                    # to improve analysis
                    shutil.rmtree(pathy)
                else:
                    # skip directories
                    continue
            else:
                if os.path.isfile(pathy):
                    #print("Now deleting..."+pathy)
                    mfile.write(pathy)
                    mfile.write('\n')
                    mfile.write(' \n')
                    if moveNotDelete:
                        # move files to another dir. 
                        # I imagine this option will really only be used 
                        # when one doesn't want to delete files that were search results 
                        # but NOT NLP matches, hence target_dir isn't an input arg (yet) 
                        target_dir = os.path.join(files_path,"no-NLP-match")
                        if not os.path.exists(target_dir):
                           os.makedirs(target_dir)
                        shutil.move(pathy, target_dir)
                    else: 
                       os.remove(pathy)
      mfile.close()

  def get_dropdown_words(self):
      dropdown_words = {'English': ['Law','law','Parliament','parliament','Congress','congress','Legislation','legislation','Legislature','legislature','Document','document','Legal','legal'], 'Spanish': ['Lei','lei','Documento','documento','Congreso','congreso','Asamblea','asamblea','Legislación','legislación','Parlamento','parlamento','Legal','legal','Legislatura','legislatura']}
      words = []
      try: 
          words = dropdown_words.get(self.language)
      except:
          print("ERROR: The language "+self.language+" is currently not supported.")
     
      return(words)

  def delete_no_matches(self,specs,path=os.getcwd(),moveFiles=True): 
      ## let's move OR delete any files not saved in the matches plain text file:
      match_exceptions = []
      matches = os.path.join(self.downloadPath,'matches_'+specs+'.txt')
      matches_in_path = os.path.join(path,'matches_'+specs+'.txt')
      if os.path.exists(matches):
         with open(matches, 'r') as f:
            lines = f.readlines()
            for line in lines:
               if len(line) > 2: # blank-ish \n lines apparently have len=2 based on how I wrote this.
                  line = line.split('\n')[0]
                  match_exceptions.append(line)
      if os.path.exists(matches_in_path):
         with open(matches_in_path, 'r') as f:
            lines = f.readlines()
            for line in lines:
               if len(line) > 2: # blank-ish \n lines apparently have len=2 based on how I wrote this.
                  line = line.split('\n')[0]
                  match_exceptions.append(line)
      if moveFiles:
         self.delete_unneeded_files('no-NLP-match_'+specs,match_exceptions,files_path=path,moveNotDelete=True)
      else:
         self.delete_unneeded_files('no-NLP-match_'+specs,match_exceptions,files_path=path,moveNotDelete=False)



