from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import pprint
import config
import json

def get_all_concepts(Config):
    theApp = ClarifaiApp(api_key=Config['DEFAULT']['CLARIFAI_API_KEY'])
    result = theApp.inputs.get_all()
    imageResult = []
    for image in result:
        x = { "id": image.input_id, "concepts": image.concepts, "url": image.url}
        imageResult.append(x)
    return imageResult


if __name__ == "__main__":

    theConfig = config.getConfig('../resource/config-prd.json')
    theResult = get_all_concepts(theConfig)
    json_result = json.dumps(theResult)
    pprint.pprint(json_result)

    pprint.pprint('Completed!')
