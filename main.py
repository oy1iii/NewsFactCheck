from flask import Flask, request

from NewsDetectModel.Detection_LSTM import detecting_fake_news
from chatGpt import summary_article
# import dbManage
import searchNews
import articleValidator

app = Flask(__name__)
@app.route('/check', methods=['GET'])
def checkNews():
    article_content = request.form['message']

    if articleValidator.article_format_validate(article_content):
        article_summary = summary_article(articleValidator.article_format_clear(article_content))
        related_news = searchNews.get_news(article_summary)
        truth_probability = detecting_fake_news(article_content)

        result = {
            'Accuracy': str(truth_probability) + "%",
            'Related News': related_news,
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