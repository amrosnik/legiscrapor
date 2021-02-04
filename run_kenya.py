import argparse
from selenium import webdriver
import pandas as pd
import os
from legiscrapor.legiskenya import legisKenya
import numpy as np 

####### LET'S RUN A KENYA WEB CRAWL ####### 

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

new_kenya = legisKenya(args.driver,download_path,options)
new_kenya.checkers()

pd.options.display.max_colwidth = 1000
keywords =[ 'judicial assistance']
#keywords = ['legal aid',
#           'legal assistance']
#keywords = ['legal aid',
#           'legal assistance',
#           'legal service',
#           'judicial assistance']

website = "http://kenyalaw.org/kl/"
all_hrefs = []
for k in keywords:
   hrefs = new_kenya.search_laws(website,k)
   all_hrefs.append(hrefs)

all_hrefs = [item.split('&term=')[0] for sublist in all_hrefs for item in sublist]
## for Kenya, the hyperlinks have '&term=KEYWORD' at the end, which doesn't impact the final destination 
## of the webpage. Removing it helps us find the unique documents, since sometimes the same document 
## is found for two different keywords.

all_hrefs = np.unique(all_hrefs)
print(len(all_hrefs))
#print(all_hrefs)

new_kenya.get_pdfs(all_hrefs,path=new_kenya.downloadPath+'final',anotherLink=True)
specs = 'all-Kenya-laws'
matches_files = new_kenya.scan_pdfs(new_kenya.downloadPath+'final',keywords)  
if len(matches_files) > 0:
    print(matches_files) 
    new_kenya.print_matches(matches_files,specs)

## let's delete any files not moved into the final destination folder (which means they're duplicates): 
new_kenya.delete_unneeded_files('duplicates-'+specs,[])

new_kenya.delete_no_matches(specs,path=new_kenya.downloadPath+'final')
new_kenya.teardown()

