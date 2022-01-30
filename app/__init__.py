from flask import Flask,jsonify,render_template
from flask_restful import Resource, Api, reqparse,request

app = Flask(__name__)
api = Api(app)

UPLOAD_FOLDER="/home/prakhar/myUploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

from app import views


