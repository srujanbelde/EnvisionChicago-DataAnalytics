import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.cross_validation import train_test_split
from sklearn import naive_bayes
from sklearn.metrics import classification_report

df=pd.read_csv("preprocessed_reviews_file.csv",names=['reviewContent','rating'])
stopset=set(stopwords.words('english'))
vectorizer=TfidfVectorizer(use_idf=True,lowercase=True,strip_accents='ascii',stop_words=stopset)
y=df['rating']
X=vectorizer.fit_transform(df.reviewContent)
clf=naive_bayes.MultinomialNB()
clf.fit(X, y)
print(classification_report(X,y))

#=======================================================================================================

Review_input=np.array(["this is a very good restaurant man super amazing"])
Review_input_vector=vectorizer.transform(Review_input)
print(clf.predict(Review_input_vector))
print(clf.predict_proba(Review_input_vector))
#=======================================================================================================