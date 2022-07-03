import requests
from flask import request
from flask_restful import Resource
import json

from app.tools import Grades


class Schools(Resource):
    def get(self):
        return json.loads(open('app/schools.json', 'r', encoding="utf-8").read())


# extract grades request
class ExtractGrades(Resource):
    def post(self):
        return json.loads(Grades(request.get_data()).extract())


class GetGradesOptions(Resource):
    def post(self):
        return Grades(request.get_data()).get_options()