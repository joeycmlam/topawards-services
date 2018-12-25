from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
# from googleapiclient.discovery import build as google_build
import pprint
import json
from PIL import Image
import urllib.request
import io
import config
from clsMySysImage import mysysImage
from tool_lang import google_translate
from tool_search import google_search

# def google_search(search_term, api_key, cse_id, start, **kwargs):
#     service = google_build("customsearch", "v1", developerKey=api_key)
#     res = service.cse().list(q=search_term, lr='lang_en', cx=cse_id, searchType="image", start=start, **kwargs).execute()
#     return res


def open_result(url_link):
    with urllib.request.urlopen(url_link) as url:
        f = io.BytesIO(url.read())
        img = Image.open(f)
        img.show()

def valid_result(url, outputs, rating, search_item):
    try:
        isShow = False
        for output in outputs:
            #if output['value'] >= rating and output['name'] in search_item:
            if output['value'] >= rating:
                print ('show result: {0} - {1:10.5f} {2}'.format(output['name'], output['value'], url))
                isShow = True
                break

        if isShow:
            record = mysysImage(url)
            #open_result(url)
            return record
        else:
            return None
    except Exception as e:
        pprint.pprint(e)


def predict_by_url(url_link, app):
    try:
        dictConcepts ={}
        theModels = get_model(app)
        for aModel in theModels:
            response = aModel.predict([ClImage(url=url_link)])
            result = response['outputs'][0]['data']['concepts']
            modelName = response['outputs'][0]['model']['name']
            dictConcepts[modelName] = result

        return dictConcepts
    except Exception as e:
        print('skip: {0}'.format(url_link))


def predict_by_localfile(file, app):

    theModels = get_model(app)
    dictConcepts = {}
    for aModel in theModels:
        response = aModel.predict([ClImage(file_obj=open(file, 'rb'))])
        result = response['outputs'][0]['data']['concepts']
        modelName = response['outputs'][0]['model']['name']
        dictConcepts[modelName] = result

    return dictConcepts

def process_result(search_item, results, aApp, selfConfig):
    idx = 0
    listRecord = []
    for result in results:
        idx += 1
        print('link {0}: {1}'.format(idx, result['link']))
        outputs = predict_by_url(result['link'], aApp)
        pprint.pprint(outputs)
        aRecord = valid_result(url=result['link'], outputs=outputs, rating=selfConfig['MIN_RATING'], search_item=search_item)
        if aRecord is not None:
            listRecord.append(aRecord.url)

    json_msg = json.dumps(listRecord)
    return listRecord

def searchImage(aConfig, aSearchKey, aStartPosn):
    dest_langs=['en', 'ja', 'ko']
    input_src_lang = 'en'
    allResult = []
    for dlang in dest_langs:
        translate_result = aSearchKey
        if input_src_lang != dlang:
            translate_result = google_translate(input_key=aSearchKey, src_lang='en', dest_lang=dlang).text
        print('search: {0}'.format(translate_result))
        results = google_search(translate_result, aConfig['DEFAULT']['GOOGLE_API_KEY'],
                                aConfig['DEFAULT']['GOOGLE_CSE_ID'], aStartPosn)
        theResult = []
        for result in results['items']:
            theResult.append(result['link'])

        allResult = list(set(allResult) | set(theResult))

        json_msg = json.dumps(allResult)
    return json_msg


def predictImage(theConfig, search_item, start_posn):
    print ('First Clarifai Image Analysis...')
    #
    theApp = ClarifaiApp(api_key=theConfig['DEFAULT']['CLARIFAI_API_KEY'])
    #
    # # theModel = app.models.get('general-v1.3')
    # theModel = app.models.get('design')
    theModel = get_model(theApp)

    listResult =[]
    max_posn = theConfig['MAX_SEARCH']
    # dest_lang=['en', 'ja', 'ko','id', 'vi', 'th', 'fil']
    dest_langs=['en', 'ja', 'ko']
    input_src_lang = 'en'
    for dlang in dest_langs:
        translate_result = search_item
        if input_src_lang != dlang:
            translate_result = google_translate(input_key=search_item, src_lang='en', dest_lang=dlang).text
        print('search: {0}'.format(translate_result))
        results = google_search(translate_result, theConfig['DEFAULT']['GOOGLE_API_KEY'], theConfig['DEFAULT']['GOOGLE_CSE_ID'], start_posn)
        for aModel in theModel:
            aList = process_result(search_item, results['items'], theApp, theConfig)
            listResult = list(set(listResult)|set(aList))
    # start_posn = results['queries']['nextPage'][0]['startIndex']

    josn_msg = json.dumps(listResult)

    return josn_msg


def get_model(aApp):

    theDesignModel = aApp.models.get('design')
    theGeneralModel = aApp.models.get('general-v1.3')
    allModels = []
    allModels.append(theDesignModel)
    allModels.append(theGeneralModel)


    return allModels

def predictImageLocal(aConfig, aFileFullName):
    theApp = ClarifaiApp(api_key=aConfig['DEFAULT']['CLARIFAI_API_KEY'])

    result = predict_by_localfile(aFileFullName, theApp)

    json_msg = json.dumps(result)
    return json_msg


def predictImageUrl(aConfig, aUrl):
    theApp = ClarifaiApp(api_key=aConfig['DEFAULT']['CLARIFAI_API_KEY'])
    result = predict_by_url(aUrl, theApp)
    json_msg = json.dumps(result)

    return json_msg


if __name__ == "__main__":

    theConfig = config.getConfig('../resource/config-prd.json')

    # search_item = input('Please input the search key: ')

    # filePath = 'C:/mysys/topAwards/material/alcohol_images/'
    # fileFullName = filePath + 'b1.jpg'

    # result = predictImageLocal(theConfig, fileFullName)

    # result = predictImage(theConfig, 'sake', 1)

    # result = searchImage(theConfig, 'sake', 1)

    url_link = 'https://i.ytimg.com/vi/DtbZFzWvTIo/maxresdefault.jpg'
    result = predictImageUrl(theConfig, url_link)
    pprint.pprint(result)

    print ('Completed!')

