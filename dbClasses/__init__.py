
from app import db
from dataclasses import dataclass


# @dataclass
class ExternalDatasetsMetadata(db.Model):
    __tablename__ = "external_datasets_metadata"

    id = db.Column(db.BigInteger(), primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    contributors = db.Column(db.String())

    # metaData = db.relationship('external_datasets', backref='external_datasets_metadata', uselist=False, lazy=True)

    def __init__(self, title, description, contributors):
        self.title = title
        self.description = description
        self.contributors = contributors


# @dataclass
class ExternalDatasets(db.Model):

    __tablename__ = 'external_datasets'

    uniqueId = db.Column(db.BigInteger(), primary_key=True)
    # author = db.Column(db.String())
    # desc = db.Column(db.String())
    # commentsText = db.Column(db.String())
    # inputText = db.Column(db.String())
    locations = db.Column(db.String())
    scientificNamesGNRD = db.Column(db.String())
    scientificNamesFlashtext = db.Column(db.String())
    day = db.Column(db.String())
    month = db.Column(db.String())
    year = db.Column(db.String())
    checklistAnnotations = db.Column(db.String())
    snamesInputs = db.Column(db.String())
    locationsInputs = db.Column(db.String())
    datesInputs = db.Column(db.String())

    # permalink = db.Column(db.String())
    # thumb = db.Column(db.String())
    # fulllink = db.Column(db.String())

    uploader = db.Column(db.BigInteger())

    isValid = db.Column(db.Boolean())
    curatedSNames = db.Column(db.String(), nullable=True)
    curatedLocations = db.Column(db.String(), nullable=True)
    curatedDates = db.Column(db.String(), nullable=True)

    datasetId = db.Column(db.BigInteger(), nullable=False)

    # dataset_id = db.Column(db.Integer, db.ForeignKey('external_datasets_metadata.id'),nullable=False)

    # externalDatasetId = db.Column(db.BigInteger())

    # pname = db.Column(db.String(80), unique=True, nullable=False)
    # color = db.Column(db.String(120), nullable=False)

    def __init__(self,
                 locations, scientificNamesGNRD, scientificNamesFlashtext,
                 day, month, year, checklistAnnotations, snamesInputs,
                 locationsInputs, datesInputs, uploader, isValid,
                 curatedSNames, curatedLocations, curatedDates, datasetId):
        # self.uniqueId = uniqueId
        # self.author = author
        # self.desc = descs
        # self.commentsText = commentsText
        # self.inputText = inputText
        self.locations = locations
        self.scientificNamesGNRD = scientificNamesGNRD
        self.scientificNamesFlashtext = scientificNamesFlashtext
        self.day = day
        self.month = month
        self.year = year
        self.checklistAnnotations = checklistAnnotations
        self.snamesInputs = snamesInputs
        self.locationsInputs = locationsInputs
        self.datesInputs = datesInputs
        self.uploader = uploader

        self.isValid = isValid
        self.curatedSNames = curatedSNames
        self.curatedLocations = curatedLocations
        self.curatedDates = curatedDates
        self.datasetId = datasetId

        # self.externalDatasetId = externalDatasetId
        # self.permalink = permalink
        # self.thumb = thumb
        # self.fulllink = fulllink

        # self.color = color

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


db.create_all()
