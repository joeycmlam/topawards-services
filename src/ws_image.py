from flask import Flask, request, render_template
from flask_restful import Resource, Api
from flask_cors import CORS
import clarifai_predict as engine
import config
import os
import tool_file as file_handler
import clarifai_concepts
import json

app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})
api = Api(app)

def upload_file():
   return render_template('upload.html')


class api_root(Resource):
    def get(self):
        print('hello world!')
        return {'hello': 'world version0.0.6'}

class search_image(Resource):
    def get(self, item):
        print('search')
        theConfig = config.getConfig('../resource/config-prd.json')
        # result = engine.searchImage(theConfig, item, 1)
        response = engine.searchImageV2(theConfig, item, 1)
        return response

class searchV1(Resource):
    def get(self):
        search_item = request.args.get('item', "")
        search_posn =request.args.get('posn', "")

        theConfig = config.getConfig('../resource/config-prd.json')
        result = engine.searchImage(theConfig, search_item, search_posn)
        return result

class searchV2(Resource):
    def get(self, item, posn):
        theConfig = config.getConfig('../resource/config-prd.json')
        result = engine.searchImage(theConfig, item, posn)
        return result

class predict_by_localfile(Resource):
    def get(self, fileFullName):
        print('predict_by_localfile start...')
        theConfig = config.getConfig('../resource/config-prd.json')
        result = engine.predictImageLocal(theConfig, fileFullName)
        return result

class predict_by_url(Resource):
    def get(self, location):
        print('predict_by_url start...')
        theConfig = config.getConfig('../resource/config-prd.json')
        result = engine.predictImageUrl(theConfig, location)
        return result


class upload_image(Resource):
    def post(self):
        file = request.files['image']
        if file:
            filename = file.filename
            theConfig = config.getConfig('../resource/config-prd.json')
            # filepath =thisConfig.config['UPLOAD_FOLDER']
            filepath = '../uploads'
            file_handler.remove_files(filepath)
            filefullname = os.path.join(filepath, filename)
            file.save(filefullname)
            result = engine.predictImageLocal(theConfig, filefullname)
            return result
        else:
            return {'status': 'failed'}

class search_concepts(Resource):
    def get(self):

        return ''

class get_all_concepts(Resource):
    def get(self):
        theConfig = config.getConfig('../resource/config-prd.json')
        theResult = clarifai_concepts.get_all_concepts(theConfig)
        # json_reult = json.dumps(theResult)
        return theResult


api.add_resource(api_root, '/')
api.add_resource(get_all_concepts, '/get_concepts')
api.add_resource(search_image, '/search/<string:item>')
# api.add_resource(searchV1, '/search_v1')
# api.add_resource(searchV2, '/search_v2/<string:item>/<int:posn>')
# api.add_resource(predict_by_localfile, '/predictfile/<path:fileFullName>')
api.add_resource(predict_by_url, '/predicturl/<path:location>')
api.add_resource(upload_image, '/uploadimage')



if __name__ == '__main__':
    app.run()

