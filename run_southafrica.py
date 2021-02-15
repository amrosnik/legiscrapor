import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
import selsearch
import re
import pandas as pd 
import nlpIE
import pdf_saver as ps 
import datetime
import argparse
from legissouthafrica import legisSouthAfrica

## test for searching South Africa Parliament website for legal aid content. 
## class legisSouthAfrica was originally generated by Selenium IDE
## but I converted it to a Chromedriver for ease of use, and added lots of customization.

####### SETUP ####### 
## ARGPARSE: args for this script. 
parser = argparse.ArgumentParser(description='Extract PDFs of legislation from South African Parliament website.')
parser.add_argument('input',help='Path to input file')

args = parser.parse_args()

####### THE GOOD STUFF ####### 

new_za = legisSouthAfrica()
new_za.read_inputs(args.input)
new_za.checkers() 

pd.options.display.max_colwidth = 1000
#keywords = ['legal aid']

if new_za.webpage == 1:
    matches_constit = new_za.run_constitution(new_za.keywords)
    specs = 'SouthAfrica-constit'
    if len(matches_constit) > 0:
        print(matches_constit) 
        new_za.print_matches(matches_constit,specs)
        new_za.delete_no_matches(specs,path=new_za.downloadPath+'constit')
    else:
        new_za.delete_unneeded_files('duplicates-nomatch-'+specs,[],files_path=new_za.downloadPath+'constit',path=new_za.downloadPath)
    new_za.delete_unneeded_files('duplicates-'+specs,[],path=new_za.downloadPath)
    new_za.teardown()
elif new_za.webpage == 2: 
    matches_mandates = new_za.run_mandates(new_za.keywords)
    specs = 'SouthAfrica-mandates'
    if len(matches_mandates) > 0:
        print(matches_mandates) 
        new_za.print_matches(matches_mandates,specs)
        new_za.delete_no_matches(specs,path=new_za.downloadPath+'mandates')
    else:
        new_za.delete_unneeded_files('duplicates-nomatch-'+specs,[],files_path=new_za.downloadPath+'mandates',path=new_za.downloadPath)
    new_za.delete_unneeded_files('duplicates-'+specs,[],path=new_za.downloadPath)
    new_za.teardown()
elif new_za.webpage == 3: 
    matches_acts = new_za.run_acts(new_za.keywords)
    specs = 'SouthAfrica-acts'
    if len(matches_acts) > 0:
        print(matches_acts) 
        new_za.print_matches(matches_acts,specs)
        new_za.delete_no_matches(specs,path=new_za.downloadPath+'acts')
    else:
        new_za.delete_unneeded_files('duplicates-nomatch-'+specs,[],files_path=new_za.downloadPath+'acts',path=new_za.downloadPath)
    new_za.delete_unneeded_files('duplicates-'+specs,[],path=new_za.downloadPath)
    new_za.teardown()
elif new_za.webpage == 4: 
    matches_bills = new_za.run_bills(new_za.keywords)
    specs = 'SouthAfrica-bills'
    if len(matches_bills) > 0:
        print(matches_bills) 
        new_za.print_matches(matches_bills,specs)
        new_za.delete_no_matches(specs,path=new_za.downloadPath+'bills')
    else:
        new_za.delete_unneeded_files('duplicates-nomatch-'+specs,[],files_path=new_za.downloadPath+'bills',path=new_za.downloadPath)
    new_za.delete_unneeded_files('duplicates-'+specs,[],path=new_za.downloadPath)
    new_za.teardown()
else: 
    print("ERROR: webpage integer indicator not found. Try 1=Constitution,2=Mandates,3=Acts,4=Other Bills.")
    exit()

