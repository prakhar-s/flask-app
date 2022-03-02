from app import app

if __name__ == '__main__':
    app.run(debug=True)  # run our Flask app


#from flask import Flask,jsonify,render_template
#from flask_restful import Resource, Api, reqparse,request
# import ast


# import csv
# import pandas as pd
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# import time
# from dateparser.search import search_dates
# import requests
# from dateparser import parse
# import traceback


# global code which should execute only once when the microservice starts

# from dateparser_data.settings import default_parsers
# parsers = [parser for parser in default_parsers if parser != 'relative-time']

# print("---global code started------")
# from flashtext import KeywordProcessor
# keyword_processor = KeywordProcessor()

# wordsToExclude=[]
# stop_words = stopwords.words('english')
# numerals=[str(i) for i in range(1,10)]
# print(type(numerals[0]))
# exclude_words_file=open("exclude-words.txt","r")
# exclude_words_lines=exclude_words_file.readlines()

# for excludeWord in exclude_words_lines:
#     wordsToExclude.append(excludeWord.strip())

# wordsToExclude.extend(numerals)
# wordsToExclude.extend(stop_words)

# setOfWordstoExclude=set(wordsToExclude)
# #print(setOfWordstoExclude)


# file1 = open("extended_placenames.txt","r")

# Lines = file1.readlines()
# setOfCities=set()
# count = 0
# # Strips the newline character
# for line in Lines:
#     if(line.strip().lower() not in setOfWordstoExclude):
#         if(line.strip().lower() not in setOfCities):
#             setOfCities.add(line.strip().lower())
#             keyword_processor.add_keyword(line.strip().lower())
#     if(line.strip().lower()=="big"):
#         print(line)

#         #cities.append(line.strip().lower())
# cities=list(setOfCities)
# print(len(cities))

# keyword_processor2 = KeywordProcessor()
# file2 = open("spidernames.txt","r")
# Lines2=file2.readlines()

# for line in Lines2:
#     keyword_processor2.add_keyword(line.strip())


# print("---global code ended------")

# def extractDates(text):
#     finalDates=[]
#     results=search_dates(text,settings={'PARSERS': parsers})
#     if(results):
#         for result in results:
#             dateFields={}
#             if(result):
#                 verbatimDate=result[0]
#                 if(parse(verbatimDate,settings={'REQUIRE_PARTS': ['day', 'month', 'year']})):
#                     #print("1")
#                     parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['day', 'month', 'year']})
#                     dateFields["year"]=parseDate.year
#                     dateFields["month"]=parseDate.month
#                     dateFields["day"]=parseDate.day
#                 elif(parse(verbatimDate,settings={'REQUIRE_PARTS': ['month', 'year']})):
#                     #print("2")
#                     parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['month', 'year']})
#                     dateFields["year"]=parseDate.year
#                     dateFields["month"]=parseDate.month
#                 elif(parse(verbatimDate,settings={'REQUIRE_PARTS': ['day','month']})):
#                     #print("3")
#                     parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['day','month']})
#                     dateFields["day"]=parseDate.day
#                     dateFields["month"]=parseDate.month
#                 elif(parse(verbatimDate,settings={'REQUIRE_PARTS': ['year']})):
#                     #print("4")
#                     parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['year']})
#                     dateFields["year"]=parseDate.year
#                 elif(parse(verbatimDate,settings={'REQUIRE_PARTS': ['month']})):
#                     #print("5")
#                     parseDate=parse(verbatimDate,settings={'REQUIRE_PARTS': ['month']})
#                     dateFields["month"]=parseDate.month
#                 else:
#                     dateFields={}

#             if(dateFields):
#                 finalDates.append(dateFields)
#         return finalDates

# def extract_names(namesArray):
#     if(not namesArray):
#         return []

#     names=[]
#     for nameObject in namesArray:
#         names.append(nameObject['name'])
#     return names

# def ShortenPermalink(permalink):
#    return permalink[0:permalink.find('?')]

# def ShortenFullLink(fullLink):
#     prefix="https://www.facebook.com"
#     return (prefix+fullLink[0:fullLink.find('&')])

# def GetUniqueId(s):
#     numbers = []
#     for word in s.split("/"):
#        if word.isdigit():
#           numbers.append(int(word))
#     return numbers[0]


# app = Flask(__name__)
# api = Api(app)

# UPLOAD_FOLDER="/home/prakhar/flask-app"
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# @app.route("/ping")
# def ping():
#     return("pong")


# @app.route('/')
# def upload():
#     return render_template("file_upload_form.html")

# @app.route('/success', methods = ['POST'])
# def success():
#     if request.method == 'POST':
#         f = request.files['file']
#         print("name of the uploaded file = ",f.filename)
#         print("\n")
#         f.save(f.filename)
#         print("\n")
#         print("mimetype=",f.mimetype)
#         return render_template("success.html", name = f.filename)


# @app.route("/extract",methods=["POST"])
# def extractAll():
#     inputFileName=request.args.get('inputFile')
#     outputFilename="Second-cut-curation-sheet-1.csv" #get this also using query params
#     start = time.time()

#     fields=["Unique id","Author","Desc","Comments Text","Input Text","Locations","Scientific Names(GNRD)","Scientific Names(Flashtext)","Day","Month","Year","Permalink","Thumb","fullLink"]
#     filename = outputFilename

#     faultyPermalinksFilename="Faulty_Permalinks.csv"
#     faultyRow=["Author","Desc","Permalink"]

#     with open(filename, 'a') as csvfile:
#         csvwriter = csv.writer(csvfile)
#         csvwriter.writerow(fields)

#     with open(faultyPermalinksFilename,'a') as faultyCsvFile:
#         fcsvwriter=csv.writer(faultyCsvFile)
#         fcsvwriter.writerow(faultyRow)

#     df=pd.read_csv("curation_sample_5.1_1to100.csv")
#     df=pd.read_csv(inputFileName)

#     for i in range(len(df)):
#         try:
#             author=df.loc[i,"Author"]
#             desc=df.loc[i,"Desc"]
#             commentsText=df.loc[i,"Comments Text"]
#             inputText=df.loc[i,"Input Text"]
#             permalink=ShortenPermalink(df.loc[i,"Permalink"])
#             uniqueId=GetUniqueId(permalink)
#             thumb=df.loc[i,"Thumb"]
#             fullLink=df.loc[i,"fullLink"]
#             if(type(fullLink)==str):
#                 fullLink=ShortenFullLink(df.loc[i,"fullLink"])

#             locations=[]
#             names=[]
#             namesFromFlashtext=[]
#             dates2=[]
#             day=""
#             month=""
#             year=""
#             sep=", "
#             if(type(inputText)==str):
#                 locations=keyword_processor.extract_keywords(inputText)
#                 namesFromFlashtext=keyword_processor2.extract_keywords(inputText)
#                 dates2=extractDates(inputText)
#                 days=[]
#                 months=[]
#                 years=[]

#                 if(dates2):
#                     for dateObject in dates2:
#                         keys=dateObject.keys()
#                         if("year" in keys):
#                             years.append(str(dateObject["year"]))
#                         if("month" in keys):
#                             months.append(str(dateObject["month"]))
#                         if("day" in keys):
#                             days.append(str(dateObject["day"]))

#                     year=sep.join(years)
#                     month=sep.join(months)
#                     day=sep.join(days)

#                 query = {'text':inputText}
#                 response = requests.get('http://localhost:3006/parse',params=query)
#                 if(response.json()['names']):
#                     names=extract_names(response.json()['names'])

#             row=[uniqueId,author,desc,commentsText,inputText,sep.join(locations),sep.join(names),sep.join(namesFromFlashtext),day,month,year,permalink,thumb,fullLink]
#             with open(filename,'a') as csvfile1:
#                 csvwriter1=csv.writer(csvfile1)
#                 csvwriter1.writerow(row)

#         except Exception:
#             traceback.print_exc()
#             print(f"value of i = {i}")
#             print(f"author = {author}")
#             print(f"text={desc}")
#             print(f"permalink = {permalink}")

#             errorRow=[author,desc,permalink]

#             with open(faultyPermalinksFilename,'a') as faultyCsvFile:
#                 fcsvwriter=csv.writer(faultyCsvFile)
#                 fcsvwriter.writerow(errorRow)

#     end = time.time()
#     print(f"Runtime of the program is {end - start}")
#     return("post method")
