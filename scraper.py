import feedparser as fp
from newspaper import Article
import json
import newspaper
from time import mktime
from datetime import datetime


# Set the limit for number of articles to download
LIMIT = 50

data = {}
data['newspapers'] = {}

documents = {
	
	"documents":[]
}


with open('newspaper.json') as data_file:
	companies = json.load(data_file)


count = 1

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
		content = Article(value['link'], memoize_articles=False)
		newsPaper = {
			"link": value['link'],
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


try:
	with open('scraped_articles.json', 'w') as outfile:
		json.dump(data, outfile)
except Exception as e: print(e)


try:
	with open('articles_analyze.json', 'w') as outfile:
		json.dump(documents, outfile)
except Exception as e: print(e)





