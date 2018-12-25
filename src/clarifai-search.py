from clarifai.rest import ClarifaiApp
import pprint
from PIL import Image
import urllib.request
import io

app = ClarifaiApp(api_key='58f63802f55d48dda796b79ccf2b4792')

print('search started...')
#app.inputs.search_by_predicted_concepts(concepts=['sake'])


response = app.inputs.search_by_annotated_concepts(concepts=['sake'],value=True)


for a in response:
    pprint.pprint(a)
    pprint.pprint(a.url)
    with urllib.request.urlopen(a.url) as url:
        f = io.BytesIO(url.read())

    img = Image.open(f)

    img.show()


#app.inputs.search_by_image(url='https://samples.clarifai.com/dog1.jpeg')

#app.inputs.search_by_metadata(metadata={'key':'value'})

print('Completed!')

