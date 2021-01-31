### python class for searching for legislation data.

### global quantities:
# TODO: add more to all of these, as per WORLD guidelines! 
countries = ["USA","Mexico","Canada","Nigeria","Russia","UK","Japan"]
un_countries = ["USA","Mexico","Canada"]
areas_of_legislation = ["child labor","child marriage","gender equality"]
## TODO: list of possible languages + tiny function to check specified language is in our list of supported languages
## total number of countries expected for each topic --> dict (topic = key, number_of_countries = value)

### class attributes: 
##### [ possible other country-like attributes: continent, hemisphere, UN-prescribed stage of development]
##### special characters, or name of unicode/keyboard needed to properly represent the language?? 
class country: 
	def __init__(self,name,language):
		### name is a string representing the country name
		### websites is a dict with the links for known resources as the values, 
		#### keys as the areas of legislation (defined as a global variable)
		### keyphrases is a dict. Values are words or phrases to use in scraping the websites in self.websites. 
		#### Keys are the areas of legislation.
		self.name = name
		self.websites = dict.fromkeys(areas_of_legislation)
		self.keyphrases = dict.fromkeys(areas_of_legislation)
		self.language = language

	def setUN(self):
		if self.name in un_countries:
			self.un = 1
		else:
			self.un = 0

	def setWebsites(self,area,links):
		# TODO: write method that will create either:
		## one value in websites dict at a time, or 
		## update ALL values in websites dict in the same fxn call. 

	def setKeyphrases(self,area,phrases):
		# TODO: take similar approach as with setWebsites

	def __str__(self):
		return(f"The country is {self.name}")

       # TODO: method(s) for combing websites established by setWebsites() for a given topic 

       # TODO: method(s) for converting PDF, doc/docx, HTML text into dataFrame for a given topic 

       # TODO: method(s) for assessing if text is pertinent to a given topic 

### methods to create: 
## fxn to translate WORLD-specified data into class structure 
## put it all in a notebook, hosted in the cloud, 

## MUST WRITE TESTS FOR ALL FUNCTIONS! 
## I will first start with English language countries, for ease of use. 
