from googletrans import Translator
from langdetect import detect

def lang_detect(input_string):
    return detect(input_string)

def google_translate(input_key, src_lang, dest_lang):
    translator = Translator()
    translator = Translator(service_urls=[
        'translate.google.com',
        'translate.google.co.kr',
    ])
    return translator.translate(input_key, dest=dest_lang, src=src_lang)

if __name__ == "__main__":
    input_string = input('Please input >')

    dest_langs=['en', 'ja', 'ko','id', 'vi', 'th', 'fil']
    input_src_lang = lang_detect(input_string)
    print('source language: {0}'.format(input_src_lang))
    for dlang in dest_langs:
        if dlang != input_src_lang:
            result = google_translate(input_string, src_lang=input_src_lang , dest_lang=dlang)
            print('{0}: {1}'.format(result, result.text))

    print('Completed!')