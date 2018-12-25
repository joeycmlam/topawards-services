from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import pprint
import config


def create_input(url, listConcepts):
    try:
        app.inputs.create_image_from_url(url=url, concepts=listConcepts,
                                         allow_duplicate_url=False)
    except Exception as e:
        pprint.pprint('exception: {0)'.format(e))


def main():
    url = "https://img.thewhiskyexchange.com/900/sake_isa1.jpg"
    concepts = ['sake','beverage']
    create_input(url, concepts)


if __name__ == "__main__":
    config = config.getConfig('../resource/config-prd.json')

    app = ClarifaiApp(api_key=config['CLARIFAI_API_KEY'])
    main()
    print('Completed!')