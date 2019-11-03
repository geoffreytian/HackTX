import feedparser as fp
from newspaper import Article
import json
import newspaper
from time import mktime
from datetime import datetime
import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess

# Set the limit for number of articles to download
LIMIT = 10

data = {}
data['newspapers'] = {}

documents = {
	
	"documents":[]
}


with open('newspaper.json') as data_file:
	companies = json.load(data_file)


count = 1


def run_sample():
	try:
		# Create the BlockBlockService that is used to call the Blob service for the storage account
		block_blob_service = BlockBlobService(account_name='hacktx', account_key='1hmCn9TjWFGW2Loerw502i8AOjK59Qx7pXxFcDHCasKZHQtypcWY8xhHliW05DrpowksXeDSEMQx5mfEiDkGPw==')

		# Create a container called 'quickstartblobs'.
		container_name ='news-sentiment'
		block_blob_service.create_container(container_name)

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

		# Download the blob(s).
		# Add '_DOWNLOADED' as prefix to '.txt' so you can see both files in Documents.
		full_path_to_file2 = os.path.join(local_path, str.replace("article_text/"+local_file_name ,'.json', '_DOWNLOADED.json'))
		print("\nDownloading blob to " + full_path_to_file2)
		block_blob_service.get_blob_to_path(container_name, "article_text/"+local_file_name, full_path_to_file2)

		sys.stdout.write("Sample finished running. When you hit <any key>, the sample will be deleted and the sample "
						 "application will exit.")
		sys.stdout.flush()
		input()

		# Clean up resources. This includes the container and the temp files
		block_blob_service.delete_container(container_name)
		os.remove(full_path_to_file)
		os.remove(full_path_to_file2)
	except Exception as e:
		print(e)





# Iterate through each news company
for company, value in companies.items():
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
		paper = newspaper.build(value['link'], memoize_articles=False)

		newsPaper = {
			"link": value['link'],
			"articles": []
		}
		
		noneTypeCount = 0
		for content in paper.articles:
			
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
			if content.publish_date is None:
				print(count, " Article has date of type None...")
				noneTypeCount = noneTypeCount + 1
				if noneTypeCount > 10:
					print("Too many noneType dates, aborting...")
					noneTypeCount = 0
					break
				count = count + 1
				continue
			article = {}
			article['title'] = content.title
			article['text'] = content.text
			article['link'] = content.url
			article['published'] = content.publish_date.isoformat()
			newsPaper['articles'].append(article)

			info = {}

			if len(content.text) < 5100:
				info["id"] = company+str(count)
				info["title"] = content.title
				info['link'] = content.url
				info["language"] = "en"
				info["text"] = content.text

				documents["documents"].append(info)


				print(count, "articles downloaded from", company, " using newspaper, url: ", content.url)
				count = count + 1
				noneTypeCount = 0

				data['newspapers'][company] = newsPaper


# try:
# 	with open('scraped_articles.json', 'w') as outfile:
# 		json.dump(data, outfile)
# except Exception as e: print(e)

run_sample()

# try:
# 	with open('articles_analyze.json', 'w') as outfile:
# 		json.dump(documents, outfile)
# except Exception as e: print(e)






