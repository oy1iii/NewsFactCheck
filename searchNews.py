import re
import numpy as np
import requests
from nltk import word_tokenize
from lxml.html import fromstring
from googlesearch import search
from bs4 import BeautifulSoup
from collections import Counter

def search_news_source(searchQuerys):
    sources = []
    for query in searchQuerys:
        for result in search(query + "site:(https://news.google.com/home?hl=en-US&gl=US&ceid=US:en)", stop=5):
            sources.append(result)

    counter = Counter(sources)
    print(counter)
    most_common = counter.most_common(3)
    print(most_common)
    return [key for key, value in most_common if value > 1]

def split_article(article):
    n = 50
    words = word_tokenize(article)
    words_arr = [words[i * n:(i + 1) * n] for i in range(len(words)//n)]
    searchQuerys = []
    for split_words in words_arr:
        searchQuerys.append(" ".join(split_words))

    return searchQuerys

def get_source_article(sourceUrl):
    content = requests.get(sourceUrl)
    soup_article = BeautifulSoup(content.content, 'html.parser')

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

    print(article)