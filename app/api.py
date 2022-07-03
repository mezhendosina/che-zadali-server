from flask_restful import Resource, reqparse
import json

from tools import Grades


class Schools(Resource):
    def get(self):
        return json.loads(open('/home/mezhendosina/mysite/schools.json', 'r', encoding="utf-8").read())


# extract grades request
class ExtractGrades(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("html")
        params = parser.parse_args()
        return Grades(params["html"]).extract()


class GetGradesOptions(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("html")
        params = parser.parse_args()
        return Grades(params["html"]).get_options()
