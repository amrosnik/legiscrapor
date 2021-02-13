"""
Test for searching South Africa Parliament website for legal aid content.

The class legisSouthAfrica was originally generated by Selenium IDE.
However, it has been converted to a Chromedriver for ease of use,
and added lots of custom functionality.
"""

import argparse

import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

# from legiscrapor import nlpIE
# from legiscrapor import pdf_saver as ps
# from legiscrapor import selsearch
from legiscrapor.legissouthafrica import legisSouthAfrica

# import datetime
# import re
# import time
import os

# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait




# ARGPARSE: args for this script.
docstring = 'Extract legislation PDFs from South African Parliament website.'
webpage_help = """
Select from:
1=Constitution
2=Mandates
3=Acts
4=Other Bills
"""

parser = argparse.ArgumentParser(description=docstring)
parser.add_argument('webpage', metavar='webpage', type=int,
                    help='Webpage to process.' + webpage_help)
parser.add_argument('--driver', '-d', default=ChromeDriverManager().install(),
                    help='Path for Chromedriver')
parser.add_argument('--path', '-p', default=None, help='Path for PDF downloads')

args = parser.parse_args()
if args.path is None:
    download_path = str(args.path)

else:
    download_path = 'south_africa_output'
    if not os.path.exists(download_path):
        os.mkdir(download_path)


# setting up options for Chromedriver
# mostly to ensure any PDF links automatically
# download the PDFs to download_path
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', {
    "download.default_directory": download_path,  # Default dir downloads
    "download.prompt_for_download": False,  # to auto download the file
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # don't show PDF in chrome
})

pd.options.display.max_colwidth = 1000
keywords = ['legal aid']

# keywords = ['legal aid',
#           'legal assistance',
#           'legal service',
#           'judicial assistance']

new_za = legisSouthAfrica(args.driver, download_path, options)
new_za.checkers()

if args.webpage == 1:
    matches_constit = new_za.run_constitution(keywords)
    specs = 'SouthAfrica-constit'
    new_za_const = new_za.downloadPath + '/constit'
    if len(matches_constit) > 0:
        print(matches_constit)
        new_za.print_matches(matches_constit, specs)
        new_za.delete_no_matches(specs, path=new_za_const)
    else:
        new_za.delete_unneeded_files('duplicates-nomatch-' + specs, [],
                                     files_path=new_za_const)

elif args.webpage == 2:
    matches_mandates = new_za.run_mandates(keywords)
    specs = 'SouthAfrica-mandates'
    new_za_mandates = new_za.downloadPath + '/mandates'
    if len(matches_mandates) > 0:
        print(matches_mandates)
        new_za.print_matches(matches_mandates, specs)
        new_za.delete_no_matches(specs, path=new_za_mandates)
    else:
        new_za.delete_unneeded_files('duplicates-nomatch-'+specs, [],
                                     files_path=new_za_mandates)

elif args.webpage == 3:
    matches_acts = new_za.run_acts(keywords)
    specs = 'SouthAfrica-acts'
    new_za_acts = new_za.downloadPath + '/acts'
    if len(matches_acts) > 0:
        print(matches_acts)
        new_za.print_matches(matches_acts, specs)
        new_za.delete_no_matches(specs, path=new_za_acts)
    else:
        new_za.delete_unneeded_files('duplicates-nomatch-' + specs, [],
                                     files_path=new_za_acts)

elif args.webpage == 4:
    matches_bills = new_za.run_bills(keywords)
    specs = 'SouthAfrica-bills'
    new_za_bills = new_za.downloadPath+'/bills'
    if len(matches_bills) > 0:
        print(matches_bills)
        new_za.print_matches(matches_bills, specs)
        new_za.delete_no_matches(specs, path=new_za_bills)
    else:
        new_za.delete_unneeded_files('duplicates-nomatch-'+specs, [],
                                     files_path=new_za_bills)


else:
    error_msg = 'ERROR: webpage integer indicator not found.'
    raise ValueError(error_msg + webpage_help)

new_za.delete_unneeded_files('duplicates-' + specs, [])
new_za.teardown()
