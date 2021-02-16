import argparse
from selenium import webdriver
import pandas as pd
import os
from legiskenya import legisKenya
import numpy as np 

####### LET'S RUN A KENYA WEB CRAWL ####### 

####### SETUP ####### 
## ARGPARSE: args for this script. 
parser = argparse.ArgumentParser(description='Extract PDFs of legislation from South African Parliament website.')
parser.add_argument('input',help='Path to input file')

args = parser.parse_args()

####### THE GOOD STUFF ####### 

new_kenya = legisKenya()
new_kenya.read_inputs(args.input)
new_kenya.checkers()

pd.options.display.max_colwidth = 1000
#keywords =[ 'judicial assistance']

all_hrefs = []
for k in new_kenya.keywords:
   print(k) 
   hrefs = new_kenya.search_laws(k)
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
new_kenya.delete_unneeded_files('duplicates-'+specs,[],path=new_kenya.downloadPath)

new_kenya.delete_no_matches(specs,path=new_kenya.downloadPath+'final')
new_kenya.teardown()

