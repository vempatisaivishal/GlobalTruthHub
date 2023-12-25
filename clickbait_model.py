import numpy as np
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.probability import FreqDist
import string as s
import re
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
import pickle


def tokenization(text):
    lst=text.split()
    return lst


def lowercasing(lst):
    new_lst=[]
    for i in lst:
        i=i.lower()
        new_lst.append(i)
    return new_lst


def remove_stopwords(lst):
    stop=stopwords.words('english')
    new_lst=[]
    for i in lst:
        if i not in stop:
            new_lst.append(i)
    return new_lst


def remove_punctuations(lst):
    new_lst=[]
    for i in lst:
        for j in s.punctuation:
            i=i.replace(j,'')
        new_lst.append(i)
    return new_lst


def remove_numbers(lst):
    nodig_lst=[]
    new_lst=[]
    for i in lst:
        for j in s.digits:
            i=i.replace(j,'')
        nodig_lst.append(i)
    for i in nodig_lst:
        if i!='':
            new_lst.append(i)
    return new_lst


def remove_spaces(lst):
    new_lst=[]
    for i in lst:
        i=i.strip()
        new_lst.append(i)
    return new_lst

def vect(lst):
    return tfidf.transform(lst)


def lemmatzation(lst):
    new_lst=[]
    for i in lst:
        i=lemmatizer.lemmatize(i)
        new_lst.append(i)
    return new_lst


from sklearn.feature_extraction.text import TfidfVectorizer

cb_data = pd.read_csv('C:/Users/vixha/clickbait_data.csv')
cb_data.head()


x = cb_data.headline
y = cb_data.clickbait
train_x, test_x, train_y, test_y = train_test_split(x, y, test_size=0.25, random_state=22,
                                                    stratify=cb_data['clickbait'])

train_x = train_x.apply(tokenization)
test_x = test_x.apply(tokenization)
train_x = train_x.apply(lowercasing)
test_x = test_x.apply(lowercasing)
train_x = train_x.apply(remove_stopwords)
test_x = test_x.apply(remove_stopwords)
train_x = train_x.apply(remove_punctuations)
test_x = test_x.apply(remove_punctuations)
train_x = train_x.apply(remove_numbers)
test_x = test_x.apply(remove_numbers)
train_x = train_x.apply(remove_spaces)
test_x = test_x.apply(remove_spaces)
lemmatizer = nltk.stem.WordNetLemmatizer()
train_x = train_x.apply(lemmatzation)
test_x = test_x.apply(lemmatzation)
train_x = train_x.apply(lambda x: ''.join(i + ' ' for i in x))
test_x = test_x.apply(lambda x: ''.join(i + ' ' for i in x))
tfidf=TfidfVectorizer()
train_1=tfidf.fit_transform(train_x)
test_1=tfidf.transform(test_x)
train_arr=train_1.toarray()
test_arr=test_1.toarray()


NB_MN=MultinomialNB()


NB_MN.fit(train_arr,train_y)
pred = NB_MN.predict(test_arr)



from sklearn.metrics import f1_score,accuracy_score
print("F1 score of the model")
print(f1_score(test_y,pred))
print("Accuracy of the model")
print(accuracy_score(test_y,pred))
print("Accuracy of the model in percentage")
print(accuracy_score(test_y,pred)*100,"%")


# In[29]:


import joblib

joblib.dump(NB_MN, 'clickbaitmodel.pkl')

# Load the model from the file
clickbaitmodel = joblib.load('clickbaitmodel.pkl')

# Use the loaded model to make predictions
clickbaitmodel.predict(test_arr)


# # In[ ]:




