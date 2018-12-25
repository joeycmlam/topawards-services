from googleapiclient.discovery import build
from tool_lang import google_translate

import pprint
import requests
import random

#my_api_key = "AIzaSyA77p0GjEHuJQ6fQWua8RozlOQmQGeLtCA"
#my_cse_id = "016370508091074484835:keclwekgzhk"
my_api_key = "AIzaSyDC4EqcgFcLgGhaYTwlEajVMwFoK_W0hUA"
my_cse_id = "007651206429417518186:lvfkdeaxiz0"

def google_search(search_term, api_key, cse_id, start, **kwargs):
    # service = build("customsearch", "v1", developerKey=api_key)
    # #res = service.cse().list(q=search_term, cx=cse_id, searchType="image", **kwargs, start=start).execute()
    # res = service.cse().list(q=search_term, cx=cse_id, searchType="image", **kwargs).execute()
    # return res['items']
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, lr='lang_en', cx=cse_id, searchType="image", start=start, **kwargs).execute()
    return res



def random_start():
    number = random.randint(1,101)
    print(number)
    return number

def main():
    search_item = 'classic coke'
    translate_result = google_translate(search_item, src_lang='en', dest_lang='ja').text
    # translate_result = search_item
    results = google_search(translate_result, my_api_key, my_cse_id, 1)
    idx = 0
    for result in results['items']:
        idx +=1
        print("result {0}: {1}".format(idx, result['link']))

if __name__ == "__main__":
    main()
