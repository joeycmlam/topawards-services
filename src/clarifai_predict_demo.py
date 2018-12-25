from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
from googleapiclient.discovery import build
import pprint
import json
from PIL import Image
import urllib.request
import io
import config
import clsMySysImage
from tool_lang import google_translate



def google_search(search_term, api_key, cse_id, start, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, searchType="image", start=start, **kwargs).execute()
    return res


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
            #record = clsImage(url, outputs)
            open_result(url)
        else:
            pprint.pprint(outputs)
    except Exception as e:
        pprint.pprint(e)
        pprint.pprint(outputs)


def predict_by_url(url_link, model):
    try:
        response = model.predict([ClImage(url=url_link)])
        return response['outputs'][0]['data']['concepts']
    except Exception as e:
        print('skip: {0}'.format(url_link))

def predict_by_localfile(file, model):
    response = model.predict([ClImage(file_obj=open(file, 'rb'))])
    return response['outputs'][0]['data']['concepts']

def process_result(search_item, results, model, selfConfig):
    idx = 0
    for result in results:
        idx += 1
        print('link {0}: {1}'.format(idx, result['link']))
        outputs = predict_by_url(result['link'], model)
        valid_result(url=result['link'], outputs=outputs, rating=selfConfig['MIN_RATING'], search_item=search_item)

def predictImage(selfConfig, search_item):


    start_posn = 1
    max_posn = selfConfig['MAX_SEARCH']
    while start_posn >= 1 and start_posn < max_posn:
        print ('print start: {0}'.format(start_posn))
        results = google_search(search_item, selfConfig['DEFAULT']['GOOGLE_API_KEY'], selfConfig['DEFAULT']['GOOGLE_CSE_ID'], start_posn)
        process_result(search_item, results['items'], theModel, selfConfig)
        start_posn = results['queries']['nextPage'][0]['startIndex']


if __name__ == "__main__":

    print ('First Clarifai Image Analysis...')

    theConfig = config.getConfig('../resource/config-prd.json')
    src_lang='en'
    #dest_lang=['ja', 'ko', 'id', 'zh-tw']
    dest_lang=['ja', 'ko','id', 'vi', 'th', 'fil']

    search_item = input('Please input the search key: ')


    app = ClarifaiApp(api_key=theConfig['DEFAULT']['CLARIFAI_API_KEY'])
    theModel = app.models.get('myModel')
    # theModel = app.models.get('general-v1.3')

    for dest in dest_lang:
        translate_result = google_translate(input_key=search_item, src_lang=src_lang, dest_lang=dest)
        print('{0}: {1}'.format(dest, translate_result.text))
        predictImage(theConfig, translate_result.text)


    print ('Completed!')

