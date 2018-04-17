import pandas as pd


query_5_result=pd.read_csv("query_5_result.csv")
user_ratings=query_5_result[['restaurantID','rating_y']]
avg_user_ratings=user_ratings.groupby(['restaurantID']).mean()
max_sentiment_labels=[]
avg_user_ratings.to_csv("averaged_ratings.csv")
avg_user_ratings=pd.read_csv("averaged_ratings.csv")

for i in range(0,len(avg_user_ratings.index)):
    temp1=query_5_result.loc[(query_5_result['restaurantID']==avg_user_ratings.iloc[i,0]) & (query_5_result['Review Sentiment']=='positive')]
    temp2=query_5_result.loc[(query_5_result['restaurantID']==avg_user_ratings.iloc[i,0]) & (query_5_result['Review Sentiment']=='negative')]
    if(len(temp1.index)>len(temp2.index)):
        max_sentiment_labels.append('positive')
    else:
        max_sentiment_labels.append('negative')

avg_user_ratings['average sentiments']=max_sentiment_labels
avg_user_ratings.to_csv("query_6_result.csv")
