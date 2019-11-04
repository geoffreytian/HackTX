
from __future__ import print_function
import feedparser as fp
from newspaper import Article
import json
import newspaper
from time import mktime
import datetime
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
import csv
import datetime
import io
import os
import sys
import time

import azure.storage.blob as azureblob
import azure.batch.batch_service_client as batch
import azure.batch.batch_auth as batch_auth
import azure.batch.models as batchmodels


input_word = sys.argv[0]

print("Yes")

all_data ={}

def main_func(search_term):
	search_term = url_encode(search_term)
	browser = None
	browser = webdriver.Chrome("%AZ_BATCH_NODE_WORKING_DIR%\\chromedriver 2")
	scrapeCNN(browser, search_term)
	scrapeBBC(browser, search_term)
	scrapeFOX(browser, search_term)
	export_json()


	# Set the limit for number of articles to download
	LIMIT = 30
	data = {}
	data['newspapers'] = {}


	documents = {
		
		"documents":[]
	}


	count = 1


	# Iterate through each news company
	for company, value in all_data.items():
		if 'rss' in value:
			d = fp.parse(value['rss'])
			print("Downloading articles from ", company)

			newsPaper = {
				"rss": value['rss'],
				"link": value['link'],
				"articles": []
			}

			for entry in d.entries:
				# Check if publish date is provided, if no the article is skipped.
				# This is done to keep consistency in the data and to keep the script from crashing.
				if hasattr(entry, 'published'):
					if count > LIMIT:
						break
					article = {}
					article['link'] = entry.link
					date = entry.published_parsed
					article['published'] = datetime.fromtimestamp(mktime(date)).isoformat()
					try:
						content = Article(entry.link)
						content.download()
						content.parse()
					except Exception as e:
						# If the download for some reason fails (ex. 404) the script will continue downloading
						# the next article.
						print(e)
						print("continuing...")
						continue
					article['title'] = content.title
					article['text'] = content.text
					newsPaper['articles'].append(article)
					print(count, "articles downloaded from", company, ", url: ", entry.link)
					count = count + 1


		else:
			# This is the fallback method if a RSS-feed link is not provided.
			# It uses the python newspaper library to extract articles
			print("Building site for ", company)


			for link in value['link']:
				content = Article(link)

				newsPaper = {
					"link": link,
					"articles": []
				}
				
				noneTypeCount = 0
				
					
				if count > LIMIT:
					break
				try:
					content.download()
					content.parse()
				except Exception as e:
					print(e)
					print("continuing...")
					continue
				# Again, for consistency, if there is no found publish date the article will be skipped.
				# After 10 downloaded articles from the same newspaper without publish date, the company will be skipped.

				article = {}
				article['title'] = content.title
				article['text'] = content.text
				article['link'] = content.url
				if content.publish_date is not None:
					article['published'] = content.publish_date.isoformat()
				newsPaper['articles'].append(article)

				info = {}

				if len(content.text) < 5100:
					info["id"] = company+str(count)
					info["title"] = content.title
					info['link'] = content.url
					info['source'] = company
					info["language"] = "en"
					info["text"] = content.text

					documents["documents"].append(info)


					print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
					count = count + 1
					noneTypeCount = 0

					data['newspapers'][company] = newsPaper

	run_sample()



def url_encode(search_term):
	terms = search_term.split(' ')
	encoded = terms[0]
	for i in range(1, len(terms)):
		encoded += "%20"
		encoded += terms[i]
	return encoded


def scrapeCNN(browser, search_term):
	url = "https://www.cnn.com/search?q=" + search_term
	browser.get(url)

	try:
		myElem = WebDriverWait(browser, 3).until(
			EC.presence_of_element_located((By.CLASS_NAME, 'cnn-search__result-headline')))
		print
		"Page is ready!"
		articles = browser.find_elements_by_xpath('//div[@class="cnn-search__result-contents"]/h3/a')
		articles2 = []
		for art in articles:
			articles2.append(art.get_attribute("href"))
		articles = articles2
		writeToJson(articles, "cnn")
	except TimeoutException:
		print
		"Loading took too much time!"

def scrapeBBC(browser, search_term):
	url = 'https://www.bbc.co.uk/search?q=' + search_term + '&filter=news'
	r = requests.get(url)
	soup = BeautifulSoup(r.text, features="html.parser")
	articles = []
	for i in range(10):
		article_to_append = soup.find("a", {"id": "search-result-" + str(i)})
		if not article_to_append == None:
			articles.append(article_to_append['href'])
		else:
			break
	writeToJson(articles, "bbc")


def scrapeFOX(browser, search_term):
	url = "https://www.foxnews.com/search-results/search?q=" + search_term + "&type=story"
	browser.get(url)

	try:
		myElem = WebDriverWait(browser, 3).until(
			EC.presence_of_element_located((By.CLASS_NAME, 'ng-binding')))
		print
		"Page is ready!"
		articles = browser.find_elements_by_xpath('//a[@ng-bind="article.title"]')
		articles2 = []
		for art in articles:
			articles2.append(art.get_attribute("href"))
		articles = articles2
		writeToJson(articles, "fox")
	except TimeoutException:
		print
		"Loading took too much time!"


def writeToJson(articles, newsSource):
	data = {
		"link": []
	}
	for art in articles:
		data['link'].append(art)
	print(data)
	all_data[newsSource] = data


def export_json():
	with open('articles.json', 'w') as fp:
		json.dump(all_data, fp)



def run_sample():
	try:
		# Create the BlockBlockService that is used to call the Blob service for the storage account
		block_blob_service = BlockBlobService(account_name='hacktx', account_key='1hmCn9TjWFGW2Loerw502i8AOjK59Qx7pXxFcDHCasKZHQtypcWY8xhHliW05DrpowksXeDSEMQx5mfEiDkGPw==')

		# Create a container called 'quickstartblobs'.
		container_name ='news-sentiment'
		block_blob_service.create_container(container_name, fail_on_exist=False)

		# Set the permission so the blobs are public.
		block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

		# Create a file in Documents to test the upload and download.
		local_path=os.path.expanduser("~/Articles")
		local_file_name ="articles_" + str(uuid.uuid4()) + ".json"
		full_path_to_file =os.path.join(local_path, local_file_name)

		print(full_path_to_file)

		try:
			with open(full_path_to_file, 'w+') as outfile:
				json.dump(documents, outfile)
				print("Yes")
		except Exception as e: print(e)

		# Write text to the file.
		# file = open(full_path_to_file,  'w')
		# file.write("Hello, World!")
		# file.close()

		print("Temp file = " + full_path_to_file)
		print("\nUploading to Blob storage as blob" + local_file_name)

		# Upload the created file, use local_file_name for the blob name
		block_blob_service.create_blob_from_path(container_name, "article_text/"+local_file_name, full_path_to_file)

		# List the blobs in the container
		print("\nList blobs in the container")
		generator = block_blob_service.list_blobs(container_name)
		for blob in generator:
			print("\t Blob name: " + blob.name)

		# # Download the blob(s).
		# # Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in Documents.
		# full_path_to_file2 = os.path.join(local_path, str.replace("article_text/"+local_file_name ,'.json', '_DOWNLOADED.json'))
		# print("\nDownloading blob to " + full_path_to_file2)
		# block_blob_service.get_blob_to_path(container_name, "article_text/"+local_file_name, full_path_to_file2)

		# sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
		# 				 "application will exit.")
		# sys.stdout.flush()
		# input()

		# # Clean up resources. This includes the container and the temp files
		# block_blob_service.delete_container(container_name)
		# os.remove(full_path_to_file)
		# os.remove(full_path_to_file2)
	except Exception as e:
		print(e)


main_func(input_word)

