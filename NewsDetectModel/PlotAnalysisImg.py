import pickle
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
import DataPreProcess
from keras.utils import pad_sequences
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix
from keras.models import load_model

data_frame = DataPreProcess.train_df

true_text = ' '.join(data_frame[data_frame['label']==0]['text'])
true_string = true_text.split(" ")

false_text = ' '.join(data_frame[data_frame['label']==1]['text'])
false_string = false_text.split(" ")

def draw_n_gram(string,i):
    n_gram = (pd.Series(nltk.ngrams(string, i)).value_counts())[:15]
    n_gram_df=pd.DataFrame(n_gram)
    n_gram_df = n_gram_df.reset_index()
    n_gram_df = n_gram_df.rename(columns={"index": "word", 0: "count"})
    print(n_gram_df.head())
    plt.figure(figsize = (16,9))
    return sns.barplot(x='count',y='word', data=n_gram_df)

draw_n_gram(true_string,1)
draw_n_gram(false_string,1)

fig,(true_ax, false_ax)=plt.subplots(1,2, figsize=(12,8))
text_len=data_frame[data_frame['label']==0]['text'].str.split().map(lambda x: len(x))
true_ax.hist(text_len,color='SkyBlue', range=[0, 10000],)
true_ax.set_title('Fake news text')
text_len=data_frame[data_frame['label']==1]['text'].str.split().map(lambda x: len(x))
false_ax.hist(text_len,color='PeachPuff', range=[0, 10000],)
false_ax.set_title('Real news text')
fig.suptitle('Words in texts')
plt.show()

chart=sns.countplot(x='label', data=data_frame, palette='Blues_r')
plt.title("Fake VS Ture",
          fontsize='20',
          backgroundcolor='aliceblue',
          color='blue');
plt.ylabel('Count of News Articles', size=15)
plt.show()


y = data_frame["label"]
x = data_frame["text"]

y = y.apply(lambda x: 0 if x == 1 else 1)

with open(r'C:\Users\user\Documents\NewsFactCheck\NewsDetectModel\tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

maxlength = 700
x = tokenizer.texts_to_sequences(x)
x = pad_sequences(x, maxlen=maxlength)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.30, random_state=24, shuffle =True)

model = load_model(r'C:\Users\user\Documents\NewsFactCheck\NewsDetectModel\model_Vec_Lsmt.h5')

y_pred_res = (model.predict(x_test) > 0.5).astype("int")

y_pred = []

for i in y_pred_res:
    if i >= 0.5:
        y_pred.append(1)
    else:
        y_pred.append(0)

print('Accuracy score:', accuracy_score(y_pred, y_test))

matrix = confusion_matrix(y_pred, y_test, normalize='all')
plt.figure(figsize=(16, 10))
ax= plt.subplot()
sns.heatmap(matrix, annot=True, cbar=False, ax = ax)

# labels, title and ticks
ax.set_xlabel('Predicted Labels', size=20)
ax.set_ylabel('True Labels', size=20)
ax.set_title('Confusion Matrix', size=20)
ax.xaxis.set_ticklabels([0,1], size=15)
ax.yaxis.set_ticklabels([0,1], size=15)
plt.show()