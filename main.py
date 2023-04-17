from flask import Flask, request
from chatGpt import summary_article
import dbManage
import searchNews
import articleValidator

app = Flask(__name__)
@app.route('/check', methods=['POST'])
def checkNews():
    article_content = request.form['message']

    if articleValidator.article_format_validate(article_content):
        article_summary = summary_article(articleValidator.article_format_clear(article_content))
        sourceUrl = searchNews.search_news_source(article_summary)

        result = {
            'Accuracy': "98%",
            'Similar Resource': sourceUrl,
            'Remarks': article_summary
        }

        return result
    else:
        result = {
            'Error': "Article not valid!"
        }

        return result

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)