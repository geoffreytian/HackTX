import requests
# pprint is used to format the JSON response
from pprint import pprint
import json
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from azure.storage import CloudStorageAccount




key_var_name = '5cae07ed5d1248f5bf2ba0a1cce9174b'
subscription_key = key_var_name

endpoint_var_name = 'https://news-sentiment.cognitiveservices.azure.com/'
endpoint = endpoint_var_name

sentiment_url = endpoint + "/text/analytics/v2.1/sentiment"


try:
	# Create the BlockBlockService that is used to call the Blob service for the storage account
	block_blob_service = BlockBlobService(account_name='hacktx', account_key='1hmCn9TjWFGW2Loerw502i8AOjK59Qx7pXxFcDHCasKZHQtypcWY8xhHliW05DrpowksXeDSEMQx5mfEiDkGPw==')
	# Create a container called 'quickstartblobs'.
	container_name ='news-sentiment'
	generator = block_blob_service.list_blobs(container_name,prefix="article_text/")

	for blob in generator:
		blob_item= block_blob_service.get_blob_to_bytes(container_name,blob.name)
		documents = blob_item.content

		new_str = json.loads(documents.decode('utf-8'))

		headers = {"Ocp-Apim-Subscription-Key": subscription_key}
		response = requests.post(sentiment_url, headers=headers, json=new_str)
		sentiments = response.json()
		pprint(sentiments)

		local_file_name ="sentiment_" + blob.name

		print("\nUploading to Blob storage as blob" + local_file_name)

		# Upload the created file, use local_file_name for the blob name
		block_blob_service.create_blob_from_bytes(container_name, local_file_name,json.dumps(sentiments).encode())


		# try:
		# 	with open("sentiment_scores/"+local_file_name, 'w+') as outfile:
		# 		json.dump(sentiments, outfile)
		# except Exception as e: print(e)

except Exception as e:
		print(e)