import argparse
from selenium import webdriver
import pandas as pd
import os
from legisweb_class import legisWeb
import numpy as np 

####### LET'S RUN A GENERIC WEB CRAWL ####### 
## Please note that this will not lead to an entirely "successful" 
## web crawl -- that is, this merely is to show the structure 
## of a run_X.py script, since it will not lead to any downloaded PDFs. 

####### SETUP ####### 
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

####### THE GOOD STUFF ####### 

new_web = legisWeb(args.driver,download_path,options)
new_web.checkers()

pd.options.display.max_colwidth = 1000
keywords =[ 'judicial assistance']

website = "http://kenyalaw.org/kl/"
all_hrefs = []
for k in keywords:
   hrefs = new_web.search_laws(website,k)
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
      new_web.delete_unneeded_files('duplicates-'+specs,[])
 
      new_web.delete_no_matches(specs,path=new_web.downloadPath+'final')
   else: 
      print("womp womp. This search didn't lead to any documents with our keywords in them!") 
else: 
    print("womp womp. This search didn't lead to any documents with our keywords in them!") 

new_web.teardown()

