from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

class api_root(Resource):
    def get(self):
        return {'hello': 'world'}


class Employee(Resource):
    def get(self):
        return {'employee': 'world'}

class search_image(Resource):
    def get(self, search_key):
        return {'search-key': search_key}


api.add_resource(api_root, '/')
api.add_resource(Employee, '/employee')
api.add_resource(search_image, '/search/<search_key>')

if __name__ == '__main__':
    app.run(port=5002)

