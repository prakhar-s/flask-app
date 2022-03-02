
from app import db


class ExternalDatasets(db.Model):

    __tablename__ = 'external_datasets'

    uniqueId = db.Column(db.BigInteger(), primary_key=True)
    #author = db.Column(db.String())
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

    # userId=db.Column(db.BigInteger())
    # externalDatasetId=db.Column(db.BigInteger())

    # pname = db.Column(db.String(80), unique=True, nullable=False)
    # color = db.Column(db.String(120), nullable=False)

    def __init__(self,
                 locations, scientificNamesGNRD, scientificNamesFlashtext,
                 day, month, year, checklistAnnotations, snamesInputs, locationsInputs, datesInputs):
        #self.uniqueId = uniqueId
        #self.author = author
        # self.desc = desc
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
        # self.permalink = permalink
        # self.thumb = thumb
        # self.fulllink = fulllink

        # self.color = color


# db.create_all()
