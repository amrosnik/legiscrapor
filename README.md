# legiscrapor: a way to scrape legislation from legislative websites around the world

legiscrapor is a project to web scrape and crawl through 
parliamentary websites of various countries around the world 
for legislation related to human rights issues. 
This is being done in conjunction with a non-profit that publishes 
open comparative datasets on legislation around the world. 

This codebase is a collection of Python modules and scripts. 
Selenium is heavily employed to automate clicking through websites. 
We assume one can find relevant legislation for a topic by downloading PDFs 
found by searching the website's database for specific keywords, 
and then using natural language processing (NLP) information exraction (IE) 
to tokenize the text and search for *actual* instances of those keywords. 
Believe it or not, some website search engines lead to results that don't 
actually contain those keywords!

The modules are as follows: 
* **nlpIE.py** : module for NLP IE 
* **pdf_saver.py** : code that reads in PDF files and executes NLP IE code. 
When a PDF is unreadable as a PDF, it converts the PDF to images, which 
are then read for text, and that text is funneled into nlpIE. 
* **selsearch.py** : module for keyword searches on HTML website source code 
and for keywords searches in hyperlink attributes.  

The code was developed originally to scrape select websites in English, 
with the principal designs based on scraping South Africa and Kenya's 
legislative websites. There is skeleton code to outline how additional languages 
may be added. 

The parent class **legisWeb** takes the most generic concepts applicable across
country websites and formalizes them; this is saved in **legisweb_class.py**. 
For countries where the specific 
website mechanics were explored and utilized, there are child classes:
**legisSouthAfrica** and **legisKenya**, for example. The child classes 
can be found in **legisX.py** files, where "X" is the country name in lowercase 
letters with no non-letter characters.

The code for actually running an end-to-end web crawl is found in **run_X.py** files. 
Currently these take input arguments from the command line, but hopefully 
this will change soon to take a more easily customizable list of inputs 
from a plain text file. 

The general usage is:
> python run_X.py /path/to/chromedriver -path /path/to/downloads/

The downloads folder need not exist prior to running the script. 
Please install both Selenium and ChromeDriver before using this. 
**It's important to have a slash at the end of the downloads path!** 

There is an extra argument for South Africa for now, because its website 
has legislation in different sections, and that additional arg specifies which 
section to peruse. So, for South Africa, one would run 
> python run_southafrica.py /path/to/chromedriver num_code -path /path/to/downloads/

where **num_code** is one of four integers: 1 (to get the Constitution), 2 (to get Mandates), 3 (to get Acts), or 4 (for Bills). 
