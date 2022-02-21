import time
from dateparser.search import search_dates
import requests
from dateparser import parse
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from dateparser_data.settings import default_parsers
from flashtext import KeywordProcessor

keyword_processor = KeywordProcessor()
keyword_processor2 = KeywordProcessor()
parsers = [parser for parser in default_parsers if parser != 'relative-time']

def populatePlaceNames():    
    print("---global code started------")

    wordsToExclude=[]
    stop_words = stopwords.words('english')
    numerals=[str(i) for i in range(1,10)]
    print(type(numerals[0]))
    exclude_words_file=open("exclude-words.txt","r")
    exclude_words_lines=exclude_words_file.readlines()

    for excludeWord in exclude_words_lines:
        wordsToExclude.append(excludeWord.strip())

    wordsToExclude.extend(numerals)
    wordsToExclude.extend(stop_words)

    setOfWordstoExclude=set(wordsToExclude)

    file1 = open("extended_placenames.txt","r")

    Lines = file1.readlines()
    setOfCities=set() 
    count = 0
    # Strips the newline character
    for line in Lines:
        if(line.strip().lower() not in setOfWordstoExclude):
            if(line.strip().lower() not in setOfCities):
                setOfCities.add(line.strip().lower())
                keyword_processor.add_keyword(line.strip().lower())
        if(line.strip().lower()=="big"):
            print(line)
                
            #cities.append(line.strip().lower())
    cities=list(setOfCities)
    print(len(cities))

def populateSpidernames():
    file2 = open("spidernames.txt","r")
    Lines2=file2.readlines()
    for line in Lines2:
        keyword_processor2.add_keyword(line.strip())

def getLocations(text):
    locations=keyword_processor.extract_keywords(text)
    return(locations)

def getScientificNamesFlashtext(text):
    names=keyword_processor2.extract_keywords(text)
    return(names)


def getScientificNamesGnfinder(inputText):
    names=[]
    query = {'text':inputText}
    response = requests.get('http://localhost:3006/parse',params=query)
    print("names is = ",)
    if(response.json()['names']):
        names=extract_names(response.json()['names'])
        print(names)
    return names

def getDates(text):
    finalDates=[]
    results=search_dates(text,settings={'PARSERS': parsers})
    if(results):
        for result in results:
            dateFields={}
            if(result):
                verbatimDate=result[0]
                if(parse(verbatimDate,settings={'REQUIRE_PARTS': ['day', 'month', 'year']})):
                    #print("1")
                    parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['day', 'month', 'year']})
                    dateFields["year"]=parseDate.year
                    dateFields["month"]=parseDate.month
                    dateFields["day"]=parseDate.day
                elif(parse(verbatimDate,settings={'REQUIRE_PARTS': ['month', 'year']})):
                    #print("2")
                    parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['month', 'year']})
                    dateFields["year"]=parseDate.year
                    dateFields["month"]=parseDate.month
                elif(parse(verbatimDate,settings={'REQUIRE_PARTS': ['day','month']})):
                    #print("3")
                    parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['day','month']})
                    dateFields["day"]=parseDate.day
                    dateFields["month"]=parseDate.month
                elif(parse(verbatimDate,settings={'REQUIRE_PARTS': ['year']})):
                    #print("4")
                    parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['year']})
                    dateFields["year"]=parseDate.year
                elif(parse(verbatimDate,settings={'REQUIRE_PARTS': ['month']})):
                    #print("5")
                    parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['month']})
                    dateFields["month"]=parseDate.month
                else:
                    dateFields={}

            if(dateFields):
                finalDates.append(dateFields)                               
        return finalDates

def extract_names(namesArray):
    if(not namesArray):
        return []
        
    names=[]
    for nameObject in namesArray:
        names.append(nameObject['name'])
    return names

def ShortenPermalink(permalink):
   return permalink[0:permalink.find('?')]

def ShortenFullLink(fullLink):
    prefix="https://www.facebook.com"
    return (prefix+fullLink[0:fullLink.find('&')])

def GetUniqueId(s):
    numbers = []
    for word in s.split("/"):
       if word.isdigit():
          numbers.append(int(word))
    return numbers[0]


populatePlaceNames()
populateSpidernames()
