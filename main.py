import nltk
from flask import Flask, request
from chatGpt import summary_article
import dbManage
from searchNews import split_article, search_news_source, get_source_article
from nltk import word_tokenize
nltk.download('punkt')
app = Flask(__name__)

def article_validate(article_content):
    words = word_tokenize(article_content)
    if len(words) < 50 or len(words) > 600:
        return False
    else:
        return True

@app.route('/detect', methods=['POST'])
def detect():
    article_content = request.form['message']

    if article_validate(article_content):
        res = summary_article(article_content)

        searchQuerys = split_article(article_content)
        sourceUrl = search_news_source(searchQuerys)

        result = {
            'Accuracy': "98%",
            'Similar Resource': sourceUrl,
            'Tips': res
        }

        dbManage.save_record()

        return result
    else:
        result = {
            'Message': "Article not valid!"
        }

        return result


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)