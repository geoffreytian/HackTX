from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import urllib.request
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json

all_data ={}
def main():
    search_term = 'Lebron James Lakers'
    search_term = url_encode(search_term)
    browser = None
    browser = webdriver.Chrome()
    scrapeCNN(browser, search_term)
    scrapeBBC(browser, search_term)
    scrapeFOX(browser, search_term)
    export_json()


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



if __name__ == '__main__':
    main()