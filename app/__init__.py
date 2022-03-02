from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api, reqparse, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER = "/home/prakhar/myUploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://biodiv:prharasr@localhost/biodiv'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from app import views