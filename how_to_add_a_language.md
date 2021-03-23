# How to add a new language to legiscrapor

This document is a brief outline of how to add a new language 
to legiscrapor. Legiscrapor currently only supports English, 
but it has been written so that it is relatively straightforward 
for that to change! 

## 1. Add a new language in the nlpIE module

Add a new `elif` block to the conditional blocks of 
the method `load_lang_model()`. Please specify a recognizable 
way to refer to the new language in the variable `lang` -- for example, 
English is called "English".  

Within the new `elif` block, attempt to load the appropriate `spacy` library.
Please follow the exception handling convention established for English.  
A list of up-to-date language supported in `spacy` language models is [here](https://spacy.io/usage/models),
along with how to refer to them in the `spacy.load()` function call.  

Lastly, as a final detail: update the `ValueError` raised so that it precisely states 
which languages the codebase now supports. 

## 2. Add a new item to the dictionary in get_dropdown_words() 
  
The method `get_dropdown_words()` of the parent class `legisWeb` contains 
a dictionary, `dropdown_words`, that saves common legislative words 
for a given language. The key is the name of the language, and the value 
is a list of these legislative words. For English, this looks like 
      
```python        
dropdown_words = {'English': ['Law','law','Parliament','parliament','Congress','congress','Legislation','legislation','Legislature','legislature','Document','document','Legal','legal']}
```
Note that this is case-sensitive. Simply add a new item to the dictionary, 
following this convention. Commas separate items in a dictionary. 
Please use the same name for 
the new language as used for the `lang` variable in `nlpIE`.

## 3. Update class attributes for websites using the new language
 
If you have created a new child class for a new website using 
this language, in the `__init__()` method, please specify the language. 
There are examples of how to do this in `legisWeb`, `legisKenya`,
and `legisSouthAfrica`. 

Please use the same name for the new language as used in previous steps!

## 4. Specify the new language in input files 

In the language section of your plain text input file, please specify 
the language of the website to be scraped.

Please use the same name for the new language as used in previous steps!

## 5. Add testing! 

Please add new unit and integration tests appropriately! Follow the examples 
of testing that will exist soon. This is a systematic way to ensure 
your own use case will work, as well as the use cases of anyone else wanting 
to legiscrape in that language!

Please use the same name for the new language as used in previous steps!
