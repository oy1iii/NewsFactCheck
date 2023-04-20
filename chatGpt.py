import openai

openai.api_key = ''

messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]

def summary_article(article_content):
    # message = input("User : ")
    if article_content:
        messages.append(
            {"role": "user", "content": "Summarize key points of the news article: " + article_content},
            # {"role": "user", "content": "Please use less than 100 words analyze whether the article contains false or misleading information:" + article_content},
            # {"role": "user", "content": "Please provide urls that are similar to the following news articles, do not need to provide the urls if the article contains false or misleading information, please analyze objectively:" + message},
            # {"role": "user", "content": "can you compare the following news articles to website articles [https://www.reuters.com/world/leaked-us-intel-document-claims-serbia-agreed-arm-ukraine-2023-04-12/] and analyze how similar the content of the articles is, expressed as a percentage:" + message},
        )
        chat = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=messages
        )

    return chat.choices[0].message.content
    # print(f"ChatGPT: {reply}")
    # messages.append({"role": "assistant", "content": reply})
