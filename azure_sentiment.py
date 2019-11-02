import requests
# pprint is used to format the JSON response
from pprint import pprint
import os
import json


with open('articles_analyze.json') as data_file:
    documents = json.load(data_file)



key_var_name = '2bfb02d195874437ad0def7e8627391d'
# if not key_var_name in os.environ:
#     raise Exception('Please set/export the environment variable: {}'.format(key_var_name))
subscription_key = key_var_name

endpoint_var_name = 'https://election-news.cognitiveservices.azure.com/'
# if not endpoint_var_name in os.environ:
#     raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = endpoint_var_name

sentiment_url = endpoint + "/text/analytics/v2.1/sentiment"


headers = {"Ocp-Apim-Subscription-Key": subscription_key}
response = requests.post(sentiment_url, headers=headers, json=documents)
sentiments = response.json()
pprint(sentiments)


try:
	with open('sentiment_scores.json', 'w') as outfile:
		json.dump(sentiments, outfile)
except Exception as e: print(e)