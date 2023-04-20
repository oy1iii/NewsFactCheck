import decimal
import warnings
warnings.filterwarnings("ignore")
import pickle
import re
import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from numpy import loadtxt
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from sklearn.model_selection import train_test_split
from keras.preprocessing import text, sequence
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score

# var = input("Please enter the news article you want to verify: ")

stop = stopwords.words('english')
lemmatizer = nltk.stem.WordNetLemmatizer()
def lemmatize_text(text):
    words = [lemmatizer.lemmatize(w) for w in word_tokenize(text)]
    return " ".join(words)

def remove_stop(text):
    words = [word for word in word_tokenize(text) if not word in stopwords.words()]
    return " ".join(words)

def wordopt(text):
    text = text.lower()
    text = re.sub('[^\w\s]', '', text)
    text = re.sub('\w*\d\w*', '', text)
    text = re.sub('\n\n', '', text)
    return text

#function to run for prediction
def detecting_fake_news(var):
    var = remove_stop(var)
    var = lemmatize_text(var)
    var = wordopt(var)

    #retrieving the best model for prediction call
    model = load_model(r'C:\Users\user\Documents\NewsFactCheck\NewsDetectModel\model_Vec_Lsmt.h5')
    max_features = 10000
    maxlen = 700

    data = {"text": [var]}

    with open(r'C:\Users\user\Documents\NewsFactCheck\NewsDetectModel\tokenizer.pickle', 'rb') as handle:
        loaded_tokenizer = pickle.load(handle)

    test = loaded_tokenizer.texts_to_sequences(data["text"])

    x_train = pad_sequences(test, maxlen=maxlen)

    prediction = model.predict(x_train)[0][0]

    return format(prediction * 100, ".2f")

    # print("The truth probability is ", format(prediction * 100, ".2f"))





