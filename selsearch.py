from selenium import webdriver
import re 
import pandas as pd 

#### Selenium function module ####

## given the entire HTML source code for a page (whole_page), 
## search for keywords (keywords; list of strings). 
## raise a warning for keywords whose counts fall below a threshold (min_count; default value = 3) 
def search_for_keywords(whole_page,keywords,min_count=3):
    total_count = 0 
    counts = dict() 
    for word in keywords:
       num_counted = whole_page.count(word)
       counts.update({word : num_counted})
       if num_counted < min_count: 
          print("Warning: Found keyword *** "+word+" *** less than "+str(min_count)+ " times.")
       total_count = total_count + num_counted
    counts.update({"TOTAL" : total_count})
    if total_count < min_count:
       print("Total count of keywords was less than "+str(min_count)+" instances. This page has insufficient evidence.") 
    return(counts)

## given a ChromeDriver driver (driver), 
## and Selenium elements for hyperlinks (n_elements), 
## search for links that match a particular regex criterion (pattern)
## and, for those links that match pattern, search their entire HTML source for keywords (keywords; list of strings) 
def find_keywords_from_links(driver,n_elements,pattern,keywords,waittime=2,min_count=3):
   n_links = [n.get_attribute("href") for n in n_elements] # extract href -- the actual hyperlink -- from Selenium elements
   n_texts = [n.get_attribute("text") for n in n_elements] # extract text version of href
   
   matches = pd.DataFrame()
   for n in range(len(n_links)):
      match = pattern.match(n_texts[n])
      if match:
          #print("found match: ",n_texts[n],n_links[n])
          driver.implicitly_wait(waittime)
          if len(n_links[n]) > 0:
             driver.get(n_links[n])
             whole_page = driver.page_source
             match_page_count = search_for_keywords(whole_page,keywords,min_count)
             print("found this many keyword instances on a pattern match page: ",match_page_count)
             new_row = {'href': n_links[n], 'pattern': pattern, 'keyword_matches': 1}
             matches = matches.append(new_row,ignore_index=True)
             # neat trick to include a dict in a pandas dataFrame cell and retain dict structure:  
             m = matches['keyword_matches'].eq(1)
             matches.loc[m,'keyword_matches'] = [match_page_count] * m.sum()
   return(matches)
