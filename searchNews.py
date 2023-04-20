import re
import numpy as np
import requests
import urllib.request
from nltk import word_tokenize
from lxml.html import fromstring
from googlesearch import search
from bs4 import BeautifulSoup as Soup
from collections import Counter
from dateutil.parser import parse
from nltk import word_tokenize

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'}
def get_article_link(url):
    content = requests.get(url)
    return content.url
def get_news(searchQuerys):
    results = []
    loop_index = 1

    key = urllib.request.quote(searchQuerys.encode("utf-8"))
    url = 'https://news.google.com/search?q={}&hl={}'.format(key, "en")

    try:
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        page = response.read()
        content = Soup(page, "html.parser")
        articles = content.select('article')

        for article in articles:
            if loop_index >= 4:
                break

            loop_index = loop_index + 1
            desc = ""

            try:
                # news title
                try:
                    title = article.find('h3').text
                except:
                    title = None

                # date
                try:
                    date = article.find("time").text
                except:
                    date = None

                # link
                try:
                    link = 'news.google.com/' + article.find("h3").find("a").get("href")
                except:
                    link = None

                if link.startswith('https://www.youtube.com/watch?v='):
                    desc = 'video'

                # site
                try:
                    site = article.find("time").parent.find("a").text
                except:
                    site = None
                try:
                    media = article.find("div").find("a").text
                except:
                    media = None

                # result collection
                results.append({'Title': title,
                               'Description': desc,
                               'Date': date,
                               'Link': get_article_link("https://" + link),
                               'Media': media})
            except Exception as article_ex:
                print(article_ex)

        response.close()
        return results
    except Exception as request_ex:
        print(request_ex)

def get_news_by_keypoint(searchQuerys):
    sources = []
    for query in searchQuerys:
        for result in search(query + "site:(https://news.google.com/home?hl=en-US&gl=US&ceid=US:en)", stop=5):
            sources.append(result)

    counter = Counter(sources)
    most_common = counter.most_common(3)

    return [key for key, value in most_common if value > 1]

def split_article(article):
    n = 50
    words = word_tokenize(article)
    words_arr = [words[i * n:(i + 1) * n] for i in range(len(words)//n)]

    searchQuerys = []
    for split_words in words_arr:
        searchQuerys.append(" ".join(split_words))

    return searchQuerys

def get_news_article(sourceUrl):
    article = ""
    content = requests.get(sourceUrl)
    soup_article = Soup(content.content, 'html.parser')

    # regex = re.compile('.*article.*')
    body = soup_article.find_all('article')
    x = body[0].find_all('p')

    # Unifying the paragraphs
    list_paragraphs = []
    final_article = ""
    for p in np.arange(0, len(x)):
        paragraph = x[p].get_text()
        list_paragraphs.append(paragraph)
        article = " ".join(list_paragraphs)

    return article