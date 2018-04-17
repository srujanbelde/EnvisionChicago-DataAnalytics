import pandas as pd
final_pd=pd.read_csv("query_5_result.csv")
five_pd=final_pd[final_pd.rating_y == 5]
four_pd=final_pd[final_pd.rating_y == 4]
three_pd=final_pd[final_pd.rating_y == 3]
two_pd=final_pd[final_pd.rating_y == 2]
one_pd=final_pd[final_pd.rating_y == 1]
print(five_pd.groupby('Review Sentiment').count())
print(four_pd.groupby('Review Sentiment').count())
print(three_pd.groupby('Review Sentiment').count())
print(two_pd.groupby('Review Sentiment').count())
print(one_pd.groupby('Review Sentiment').count())


print("this file is used to check the number of true positives and false positives classified in each rating")

