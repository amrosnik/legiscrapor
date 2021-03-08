# legiscrapor: a way to scrape legislation from legislative websites around the world

legiscrapor is a project to web scrape and crawl through 
parliamentary websites of various countries around the world 
for legislation related to human rights issues. 
This is being done in conjunction with a non-profit that publishes 
open comparative datasets on legislation around the world. 


## Installation
`legiscrapor` can be installed with

```sh
pip install .
```
(PyPi installation available soon)

(This installation depends, of course, on cloning the repo/downloading the ZIP file first 
and running the above command from within the repo directory.)

## Development
Install the test dependencies with:

```sh
pip install .[testing]
```

This codebase is a collection of Python modules and scripts. 

Selenium is heavily employed to automate clicking through websites. 
We assume one can find relevant legislation for a topic by downloading PDFs 
found by searching the website's database for specific keywords, 
and then using natural language processing (NLP) information exraction (IE) 
to tokenize the text and search for *actual* instances of those keywords. 
Believe it or not, some website search engines lead to results that don't 
actually contain those keywords!

## Prerequisites to install

All the prereqs are now installed through the `pip install` step, 
but for the sake of clarity, the major dependencies are: 

General software (please search for your operating system for instructions):
* Chromedriver 
* webdriver-manager

Python packages (these all can be installed via `pip`, and probably other alternatives): 
* selenium
* numpy
* pandas
* spacy
* pytesseract
* wand.image 

A crucial Python package to install is `spacy` for Python-friendly natural language models. Check the [spacy website](https://spacy.io/usage) for updated installation instructions. It requires `pip`, but it is important to first install `setuptools` and `wheel`, as well as download *all* necessary language models prior to running this package. Currently the `nlpIE` module attempts to download any necessary but missing language models; please follow that convention when adding more language models to the codebase.  

## Modules 

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

## Execution instructions

The code for actually running an end-to-end web crawl is found in **run_X.py** files. 
These take input arguments from a plain text file. See `inputs/` for example input files. 

The general usage is:
> python run_X.py /path/to/input_file 
**It's important to have a slash at the end of the downloads path!** 

The downloads folder need not exist prior to running the script. 
Please install both Selenium and ChromeDriver before using this.
For linux:

```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

For Windows: look at [this guide](http://jonathansoma.com/lede/foundations-2018/classes/selenium/selenium-windows-install/). 

