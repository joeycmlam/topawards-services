from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import pprint

print ('First Clarifai Image Analysis...')

app = ClarifaiApp(api_key='58f63802f55d48dda796b79ccf2b4792')

model = app.models.get('general-v1.3')
image = ClImage(file_obj=open('../../../images/top-hp-001.jpg','rb'))

#response=model.predict([image])

response=model.predict([ClImage(file_obj=open('../../../images/top-hp-001.jpg','rb'))])

pprint.pprint(response)

counter = 0
for row in response['concepts']:
    counter += 1
    print('Label ' + str(counter) + ': ' + row['name'] + ',' + str(row['value']))


print ('Completed!')
