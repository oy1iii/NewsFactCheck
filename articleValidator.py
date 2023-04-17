from nltk import word_tokenize

def article_format_validate(article_content):
    words = word_tokenize(article_content)
    if len(words) > 600 or not article_content:
        return False
    else:
        return True

def article_format_clear(article_content):
    return  article_content.strip()