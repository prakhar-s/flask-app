from crypt import methods
import dataclasses
import time

from sqlalchemy import false, true
from app import app
from flask import render_template
from flask_restful import Resource, Api, reqparse, request
import pandas as pd
from dateparser.search import search_dates
from dateparser import parse
import traceback
import csv
from utils import getScientificNamesGnfinder, getScientificNamesFlashtext, ShortenPermalink, GetUniqueId, ShortenFullLink, getDates, extract_names, getLocations
from dbClasses import ExternalDatasets, ExternalDatasetsMetadata
from app import db
import json
from flask import jsonify


@app.route("/ping")
def ping():
    return("pong")


@app.route('/')
def upload():
    return render_template("file_upload_form.html")


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f = request.files['file']
        print("name of the uploaded file = ", f.filename)
        print("\n")
        f.save("/home/prakhar/myUploads/uploaded.csv")
        print("\n")
        print("mimetype=", f.mimetype)
        return render_template("success.html", name=f.filename)


@app.route("/locations", methods=["GET"])
def extractLocations():
    text = request.args.get("text")
    locations = getLocations(text)
    response = {"locations": locations}
    return(response)


@app.route("/dates", methods=["GET"])
def extractDates():
    text = request.args.get("text")
    dates = getDates(text)
    response = {"dates": dates}
    return response


@app.route("/names/gnfinder/", methods=["GET"])
def extractScientificNamesGnfinder():
    text = request.args.get("text")
    names = getScientificNamesGnfinder(text)
    response = {"names": names}
    return response


@app.route("/names/flashtext/", methods=["GET"])
def extractScientificNamesFlashtext():
    text = request.args.get("text")
    names = getScientificNamesFlashtext(text)
    response = {"names": names}
    return response


@app.route("/test", methods=["POST"])
def test():
    formData = request.form
    columnsSelected = formData.to_dict(flat=False)
    snameColumns = columnsSelected['sname'][0].split(",")
    locationColumns = columnsSelected['location'][0].split(",")
    dateColumns = columnsSelected['date'][0].split(",")

    return columnsSelected


@app.route("/show/<uploaderId>/<datasetId>", methods=["GET"])
def showPage(uploaderId, datasetId):
    ans = ExternalDatasets.query.filter_by(
        uploader=str(uploaderId), datasetId=str(datasetId)).all()

    l = []
    for row in ans:
        l.append(row.as_dict())

    print(type(ans[0].as_dict()))
    return (jsonify(l))


@app.route("/extract", methods=["POST"])
def extractAll():
    # nameTextInput=request.args.get("nameTextField")
    # locationTextInput=request.args.get("locationTextField")
    # dateTextInput=request.args.get("dateTextField")

    formData = request.form.to_dict(flat=False)

    print("formdata recieved is = ", formData)

    snameColumns = formData['sname'][0].split(",")
    locationColumns = formData['location'][0].split(",")
    dateColumns = formData['date'][0].split(",")
    inputFileName = formData['path'][0]
    title = formData['title'][0]
    datasetDescription = formData['datasetDescription'][0]
    uploaderId = formData['userId'][0]
    contributorIds = formData['contributorsIds'][0].split(",")

    sep = ", "

    print("contribuitors are = ", contributorIds)

    metdataEntry = ExternalDatasetsMetadata(
        title=title, description=datasetDescription, contributors=sep.join(contributorIds))
    db.session.add(metdataEntry)
    db.session.commit()

    print("title=", title)
    print("dataset desc=", datasetDescription)

    # inputFileName="/home/prakhar/myUploads/uploaded.csv"
    # outputFilename="Second-cut-curation-sheet-1.csv" #get this also using query params
    outputFilename = "/home/prakhar/myUploads/output.csv"
    print("-----------EXTRACTION PROCESS STARTED-------------")
    start = time.time()

    fields = ["Unique id", "Author", "Desc", "Comments Text", "Input Text", "Locations",
              "Scientific Names(GNRD)", "Scientific Names(Flashtext)", "Day", "Month", "Year", "Permalink", "Thumb", "fullLink"]
    filename = outputFilename

    faultyPermalinksFilename = "Faulty_Permalinks.csv"
    faultyRow = ["Author", "Desc", "Permalink"]

    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)

    with open(faultyPermalinksFilename, 'a') as faultyCsvFile:
        fcsvwriter = csv.writer(faultyCsvFile)
        fcsvwriter.writerow(faultyRow)

    # df=pd.read_csv("curation_sample_5.1_1to100.csv")
    df = pd.read_csv(inputFileName)

    allcolumns = list(df.columns)
    checklistAnnotationsColumns = []
    for column in allcolumns:
        if(column not in snameColumns and column not in locationColumns and column not in dateColumns):
            checklistAnnotationsColumns.append(column)

    for i in range(len(df)):

        try:
            author = df.loc[i, "Author"]
            desc = df.loc[i, "Desc"]
            commentsText = df.loc[i, "Comments Text"]
            inputText = df.loc[i, "Input Text"]
            permalink = ShortenPermalink(df.loc[i, "Permalink"])
            uniqueId = GetUniqueId(permalink)
            thumb = df.loc[i, "Thumb"]
            fullLink = df.loc[i, "fullLink"]

            nameTextInput = ""
            locationTextInput = ""
            dateTextInput = ""
            checklistAnnotations = {}
            snamesInputs = {}
            locationsInputs = {}
            datesInputs = {}

            for column in snameColumns:
                if(df.loc[i, column] != "nan"):
                    nameTextInput = nameTextInput+" | "+str(df.loc[i, column])
                    snamesInputs[column] = str(df.loc[i, column])

            for column in locationColumns:
                if(df.loc[i, column] != "nan"):
                    locationTextInput = locationTextInput + \
                        " | "+str(df.loc[i, column])
                    locationsInputs[column] = str(df.loc[i, column])

            for column in dateColumns:
                if(df.loc[i, column] != "nan"):
                    dateTextInput = dateTextInput+" | "+str(df.loc[i, column])
                    datesInputs[column] = str(df.loc[i, column])

            for column in checklistAnnotationsColumns:
                checklistAnnotations[column] = str(df.loc[i, column])

            print("name text input is=", nameTextInput)

            if(type(fullLink) == str):
                fullLink = ShortenFullLink(df.loc[i, "fullLink"])
            locations = []
            names = []
            namesFromFlashtext = []
            dates2 = []
            day = ""
            month = ""
            year = ""

            locations = getLocations(locationTextInput)
            namesFromFlashtext = getScientificNamesFlashtext(nameTextInput)
            dates2 = getDates(dateTextInput)
            days = []
            months = []
            years = []
            if(dates2):
                for dateObject in dates2:
                    keys = dateObject.keys()
                    if("year" in keys):
                        years.append(str(dateObject["year"]))
                    if("month" in keys):
                        months.append(str(dateObject["month"]))
                    if("day" in keys):
                        days.append(str(dateObject["day"]))

                year = sep.join(years)
                month = sep.join(months)
                day = sep.join(days)

            names = getScientificNamesGnfinder(nameTextInput)

            row = [uniqueId, author, desc, commentsText, inputText, sep.join(locations), sep.join(
                names), sep.join(namesFromFlashtext), day, month, year, permalink, thumb, fullLink]
            with open(filename, 'a') as csvfile1:
                csvwriter1 = csv.writer(csvfile1)
                csvwriter1.writerow(row)

            dbEntry = ExternalDatasets(locations=sep.join(locations), scientificNamesGNRD=sep.join(names),
                                       scientificNamesFlashtext=sep.join(namesFromFlashtext), day=day, month=month,
                                       year=year, checklistAnnotations=str(
                checklistAnnotations),
                snamesInputs=str(snamesInputs), locationsInputs=str(locationsInputs),
                datesInputs=str(datesInputs), uploader=uploaderId,
                isValid=True, curatedSNames="", curatedLocations="", curatedDates="", datasetId=metdataEntry.id)

            db.session.add(dbEntry)
            db.session.commit()

        except Exception:
            traceback.print_exc()
            print(f"value of i = {i}")
            print(f"author = {author}")
            print(f"text={desc}")
            print(f"permalink = {permalink}")
            print(f"fault text={nameTextInput}")
            print("checklist annotations=", checklistAnnotations)

            errorRow = [author, desc, permalink]

            with open(faultyPermalinksFilename, 'a') as faultyCsvFile:
                fcsvwriter = csv.writer(faultyCsvFile)
                fcsvwriter.writerow(errorRow)

    end = time.time()
    print("------EXTRACTION PROCESS ENDED---------------")
    print(f"Runtime of the program is {end - start}")
    return("post method")
