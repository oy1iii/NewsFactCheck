from flask import Flask, request
from flask_cors import CORS
from flask import abort
from NewsDetectModel.Detection_LSTM import detecting_fake_news
from chatGpt import summary_article
# import dbManage
import searchNews
import articleValidator

app = Flask(__name__)
CORS(app)
@app.route('/check', methods=['GET'])
def checkNews():
    # article_content = request.form['message']
    article_content = request.args.get('message')

    if articleValidator.article_format_validate(article_content):
        article_summary = summary_article(articleValidator.article_format_clear(article_content))
        related_news = searchNews.get_news(article_summary)
        truth_probability = detecting_fake_news(article_content)
        result = "success"

        if float(truth_probability) < 60.00:
            result = "error"

        result = {
            'Result': result,
            'Accuracy': str(truth_probability) + "%",
            'RelatedNews': related_news,
            'Remarks': article_summary
        }
        print(result)
        return result
    else:
        abort(404)

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 8000)