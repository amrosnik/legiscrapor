import argparse
from selenium import webdriver
import pandas as pd
import os
from legiscrapor.legisweb_class import legisWeb
import numpy as np 

####### LET'S RUN A GENERIC WEB CRAWL ####### 
## Please note that this will not lead to an entirely "successful" 
## web crawl -- that is, this merely is to show the structure 
## of a run_X.py script, since it will not lead to any downloaded PDFs. 

####### SETUP ####### 
## ARGPARSE: args for this script. 
parser = argparse.ArgumentParser(description='Extract PDFs of legislation from South African Parliament website.')
parser.add_argument('input',help='Path to input file')

args = parser.parse_args()

####### THE GOOD STUFF ####### 

new_web = legisWeb()
new_web.read_inputs(args.input)
new_web.checkers()

pd.options.display.max_colwidth = 1000
#keywords =[ 'judicial assistance']

all_hrefs = []
for k in new_web.keywords:
   hrefs = new_web.search_laws(k)
   all_hrefs.append(hrefs)

if len(all_hrefs) > 0: 
   all_hrefs = [item.split('&term=')[0] for sublist in all_hrefs for item in sublist]
   all_hrefs = np.unique(all_hrefs)
   if len(all_hrefs) > 0: # the above manipulations shouldn't yield zero links, but technically a list with one empty element has len=1, soooooooooo  
      print("found this many links:" ,len(all_hrefs))
      new_web.get_pdfs(all_hrefs,path=new_web.downloadPath+'final',anotherLink=True)
      specs = 'all-generic-laws'
      matches_files = new_web.scan_pdfs(new_web.downloadPath+'final',keywords)  
      if len(matches_files) > 0:
         print(matches_files) 
         new_web.print_matches(matches_files,specs)

      ## let's delete any files not moved into the final destination folder (which means they're duplicates): 
      new_web.delete_unneeded_files('duplicates-'+specs,[],moveNotDelete=True)
 
      new_web.delete_no_matches(specs,path=new_web.downloadPath+'final',moveFiles=True)
   else: 
      print("womp womp. This search didn't lead to any documents with our keywords in them!") 
else: 
    print("womp womp. This search didn't lead to any documents with our keywords in them!") 

new_web.teardown()

