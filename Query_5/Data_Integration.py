import pandas as pd
from textblob import TextBlob
from openpyxl.chart.series import Series
import numpy as np

restaurants_file_pd=pd.read_csv("restaurants_60601-60606.csv")
reviews_file_pd=pd.read_csv("clean_reviews_60601-60606.csv")
combined_file=pd.merge(restaurants_file_pd,reviews_file_pd,left_on="restaurantID",right_on="restaurantID")
combined_file.to_csv("restaurants_reviews_combined_file.csv", sep=',', encoding='utf-8')

combined_file_pd=pd.read_csv("restaurants_reviews_combined_file.csv")

review_sentiment=[]
for i in range(0,len(combined_file_pd.index)):
    temp=combined_file_pd.ix[i]["reviewContent"]
    blob=TextBlob(temp)
    if(blob.sentiment.polarity > 0.175):
        predict_rating="positive"
    else:
        predict_rating="negative"
    review_sentiment.append(predict_rating)

combined_file_pd['Review Sentiment']=review_sentiment

result_pd=combined_file_pd[['restaurantID','name','reviewID','Review Sentiment','rating_y']]
result_pd.to_csv("query_5_result.csv")
print("Review file and Restaurant files are combined and sentiment for each review is estimated using textblob")

